from rest_framework import permissions
from rest_framework.response import Response

from .models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
        return Response(status=403)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE' and request.user.is_authenticated:
            return request.user.role == MODERATOR
        return Response(status=403)
