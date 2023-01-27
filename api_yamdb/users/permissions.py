from rest_framework import permissions
from rest_framework.response import Response

from .models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
        return Response(status=403)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Установка разрешения на полный доступ к объекту только для автора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsModerator(IsAuthorOrReadOnly):
    """
        Установка уровня прав: модератор.
        Модератор может удалять любые отзывы и комментарии.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == MODERATOR and request.method == "DELETE"
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
