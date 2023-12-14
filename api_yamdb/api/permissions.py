from rest_framework import permissions


class IsAuthenticatedAuthororReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return True
    """ (
            obj.author == request.user
            or request.method in permissions.SAFE_METHODS
        ) """