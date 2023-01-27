from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'users'

users_router = DefaultRouter()

users_router.register(
    'users',
    views.UserViewSet,
    basename='users',
)
users_router.register(
    'signup',
    views.SignUpViewSet,
    basename='signup',
)
users_router.register(
    'token',
    views.GetJWTToken,
    basename='token',
)


urlpatterns = [
    path('', include(users_router.urls)),
    path(
        'auth/',
        include(users_router.urls)
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
]
