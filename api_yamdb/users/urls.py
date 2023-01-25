from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
v1_router.register(
    'token',
    views.GetJWTToken,
    basename='token',
)


urlpatterns = [
    path('', include(v1_router.urls)),
    path(
        'auth/',
        include(v1_router.urls)
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
]
