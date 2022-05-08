from rest_framework import permissions


class MethodPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" and view.action != "create"
