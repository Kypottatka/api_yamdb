from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


app_name = 'users'

v1_router = DefaultRouter()

v1_router.register(
    'users',
    views.UserViewSet,
    basename='users',
)
v1_router.register(
    'signup',
    views.SignUpViewSet,
    basename='signup',
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path(
        'auth/',
        include(v1_router.urls)
    ),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'auth/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
]
