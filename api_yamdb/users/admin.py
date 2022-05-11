from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "role",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")


admin.site.register(User, UserAdmin)
