from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = (
        (
            None,
            {"fields": ("email", "password")},
        ),
        (
            _("Groups"),
            {"fields": ("groups",)},
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "user_permissions"),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
    )
    filter_horizontal = ("user_permissions",)

    ordering = ("email",)
