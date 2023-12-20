from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    pass
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin
    


class IsAuthenticatedAuthororReadOnly(permissions.BasePermission):
    pass

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin
