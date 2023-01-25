from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import get_jwt_token


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
        get_jwt_token,
        name='token_obtain_pair'
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
]
