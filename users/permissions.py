from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsNotModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not IsModer().has_permission(request, view)
