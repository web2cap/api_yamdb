from rest_framework import permissions


class PostOnlyNoCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" and view.action != "create"
