from rest_framework import permissions

from rest_framework.exceptions import PermissionDenied


class IsAuthCUD(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT", "DELETE"]:
            if obj.user != request.user:
                raise PermissionDenied(
                    "Вы не являетесь владельцем этого объявления.")
            return True

        return True


class IsReciver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "PUT"]:
            return request.user == obj.ad_receiver.user
        return True
