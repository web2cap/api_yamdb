from rest_framework import permissions


class PostOnlyNoCreate(permissions.BasePermission):
    """Разрешает только метод POST. Запрещает действие метода POST create."""

    def has_permission(self, request, view):
        return request.method == "POST" and view.action != "create"


class IsRoleAdmin(permissions.BasePermission):
    """Разрешает доступ пользователям с ролью admin и суперпользователям."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin or request.user.is_superuser


class OwnerUserGetPatchOnly(permissions.BasePermission):
    """Разрешает методы GET и PATCH к обекту USER толко владельцам."""

    def has_permission(self, request, view):
        allowed_methods = ("GET", "PATCH")
        return (
            request.user.is_authenticated and request.method in allowed_methods
        )

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class MeGetPatchOnlyOrAdmin(permissions.BasePermission):
    """Разрешает методы GET и PATCH к обекту USER  владельцам.
    Полный доступ админам."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        allowed_me_methods = ("GET", "PATCH")
        path_end = request.path_info.split("/")[-2]
        return (
            (request.user.is_admin or request.user.is_superuser)
            and path_end != "me"
        ) or (request.method in allowed_me_methods and path_end == "me")
