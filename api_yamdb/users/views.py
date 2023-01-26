import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from .models import User
from .permissions import IsAdmin
from .pagination import UsersPagination


class GetJWTToken(viewsets.ModelViewSet):
    serializer_class = TokenSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        if User.objects.filter(email=email, username=username).exists():
            return Response(status=status.HTTP_200_OK)

        elif (
            User.objects.filter(email=email).exists()
                or User.objects.filter(username=username).exists()):
            return Response(
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'

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
                status=status.HTTP_200_OK,
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=['DELETE'],
    )
    def delete_user(self, request):
        if request.user.role != 'admin':
            return Response(
                {'detail': 'У вас нет прав на удаление пользователей'},
                status=status.HTTP_403_FORBIDDEN
            )
        user = get_object_or_404(User, username=request.data['username'])
        user.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Метод PUT не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)
