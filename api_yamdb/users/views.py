import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer,
    SignUpSerializer,
)
from .models import User
from .permissions import IsAdmin
from .pagination import UsersPagination


@api_view(['POST'])
def get_jwt_token(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, username=username, email=email)

        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'confirmation_code': 'Не верный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        if User.objects.filter(email=email).exists():
            return Response(
                {'email': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {'username': 'Пользователь с таким username уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        confirmation_code = uuid.uuid4()
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)

        User.objects.filter(email=email).update(
            confirmation_code=confirmation_code
        )

        mail_subject = 'Код подтверждения'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(
            mail_subject,
            message,
            f'Yamdb <{settings.EMAIL_ADMIN}>',
            [email],
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsAuthenticated,)
    pagination_class = UsersPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def get_self_user_page(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(
                serializer.data,
                status=200
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=200)

    @action(
        detail=False,
        methods=['DELETE'],
    )
    def delete_user(self, request):
        if request.user.role != 'admin':
            return Response(
                {'detail': 'У вас нет прав на удаление пользователей'},
                status=403
            )
        user = get_object_or_404(User, username=request.data['username'])
        user.delete()
        return Response(status=403)
