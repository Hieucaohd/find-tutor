from rest_framework import permissions
from ..models import ParentModel


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOfRoom(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        parent_request = ParentModel.objects.filter(user=request.user)

        if parent_request:
            return obj.parent == parent_request
        return False


class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        parent_request = ParentModel.objects.filer(user=request.user)
        if parent_request:
            return True
        return False
