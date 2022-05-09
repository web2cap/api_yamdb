from rest_framework import permissions


class PostOnlyNoCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" and view.action != "create"


class IsRoleAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return request.user.is_admin
