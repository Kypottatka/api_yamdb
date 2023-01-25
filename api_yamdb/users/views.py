import uuid

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    SendCodeSerializer,
    CheckConfirmationCodeSerializer,
)
from .models import User


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']

    if serializer.is_valid():
        confirmation_code = uuid.uuid4()
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email)

        User.objects.filter(email=email).update(
            confirmation_code=make_password(
                confirmation_code,
                salt=None,
                hasher='default'
            )
        )

        mail_subject = 'Confirmation code on Yamdb.ru'
        message = f'Your confirmation code: {confirmation_code}'
        send_mail(
            mail_subject,
            message,
            f'Yamdb.ru <{settings.EMAIL_ADMIN}>',
            [email],
        )

        return Response(
            f'Code was sent to {email}, please check',
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_jwt_token(request):
    serializer = CheckConfirmationCodeSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        confirmation_code = serializer.data['confirmation_code']
        user = get_object_or_404(User, email=email)

        if check_password(confirmation_code, user.confirmation_code):
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'confirmation_code': 'Wrong confirmation code'},
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)  # fix is required
    pagination_class = LimitOffsetPagination
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
