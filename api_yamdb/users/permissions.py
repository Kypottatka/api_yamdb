from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import ADMIN


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == ADMIN
        return Response(status=403)


class PutRequestPrevention(permissions.BasePermission):
    def has_permission(self, request):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return True
