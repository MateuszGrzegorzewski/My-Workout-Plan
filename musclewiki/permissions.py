from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class AuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.user.is_staff:
        #     return True

        if request.method in permissions.SAFE_METHODS:
            if obj.user == request.user:
                return True

            if obj.user.is_staff:
                return True

        if obj.user == request.user:
            return True

        return False
