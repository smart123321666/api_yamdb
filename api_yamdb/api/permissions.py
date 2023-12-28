from rest_framework import permissions

class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedAuthororReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.role, request.user.is_authenticated, '!!!!!!!!')
        return (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        print(request.user, '!!!!!!!!')
        return (
            obj.author == request.user
            or request.user.is_authenticated 
        )
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


# не подключен
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)
