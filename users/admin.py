from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import AuthUser, Profile


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_avatar", "city", "country", "created_at", )
    list_filter = ("country", )
    ordering = ("user", "country", "created_at", )
    search_fields = ("city", "country", )
    readonly_fields = ("display_avatar", "user_name", "user", )

    fieldsets = (
        (_("Avatar"), {"fields": ("display_avatar", "avatar", )}),
        (_("Contact Information"), {"fields": ("user_name", "user", "phone", "city", "country", )}),
    )

    def user_name(self, obj):
        if obj.user.first_name:
            return f"{obj.user.first_name} {obj.user.last_name}"

    user_name.short_description = "Full Name"

    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="%s" width="50px" />' % obj.avatar.url)

    display_avatar.short_description = "Current Avatar"
