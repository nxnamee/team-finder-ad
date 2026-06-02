"""Admin configuration for the custom User model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """User admin with profile fields."""

    list_display = ("email", "first_name", "last_name", "is_active", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личные данные",
            {
                "fields": ("first_name", "last_name", "avatar", "description", "phone", "github"),
            },
        ),
        (
            "Права доступа",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
