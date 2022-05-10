from rest_framework import permissions


class PostOnlyNoCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST" and view.action != "create"


class RoleAdminrOrReadOnly(permissions.BasePermission):
    """Доступ на чтение всем. Полный доступ админу и суперпользователю."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            is_role_adm = False
        else:
            is_role_adm = request.user.is_admin or request.user.is_superuser
        return request.method in permissions.SAFE_METHODS or is_role_adm
