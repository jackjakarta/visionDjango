from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AuthUser


@admin.register(AuthUser)
class AuthUserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", )
    ordering = ("email", "first_name", "last_name", "is_staff", )
    search_fields = ("email", "first_name", "last_name", )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Meta Information"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "email", "password1", "password2"),
            },
        ),
    )
