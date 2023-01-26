from rest_framework import permissions
from rest_framework.response import Response

from .models import ADMIN


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
        return Response(status=403)
