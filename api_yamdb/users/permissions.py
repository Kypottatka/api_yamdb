from rest_framework import permissions
from rest_framework.response import Response

from .models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
        return Response(status=403)


class PutRequestPrevention(permissions.BasePermission):
    def has_permission(self, request):
        if request.method == 'PUT':
            return Response(status=405)
        return True


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):

        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if (
                    request.user.is_staff
                    or request.user.role == ADMIN
                    or request.user.role == MODERATOR
                    or obj.author == request.user
                    or request.method == 'POST'
                    and request.user.is_authenticated
            ):
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
