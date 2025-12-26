from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-date_joined",)
    list_display = (
        "email_or_phone",
        "role",
        "is_active",
        "is_staff",
        "is_deleted",
        "is_email_verified",
        "is_phone_verified",
        "date_joined",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_deleted",
        "is_email_verified",
        "is_phone_verified",
    )
    search_fields = (
        "email_or_phone",
        "email",
        "phone",
        "username",
        "first_name",
        "last_name",
    )
    readonly_fields = (
        "user_uuid",
        "date_joined",
        "updated_at",
        "last_login_at",
        "last_login_ip",
        "failed_login_attempts",
        "token_version",
    )

    fieldsets = (
        (_("Identity"), {
            "fields": (
                "user_uuid",
                "email_or_phone",
                "email",
                "phone",
                "username",
                "first_name",
                "last_name",
            )
        }),
        (_("Verification"), {
            "fields": (
                "is_email_verified",
                "is_phone_verified",
            )
        }),
        (_("Security"), {
            "fields": (
                "password",
                "failed_login_attempts",
                "locked_until",
                "last_login_at",
                "last_login_ip",
                "token_version",
            )
        }),
        (_("Permissions & Role"), {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Lifecycle"), {
            "fields": (
                "is_deleted",
                "deleted_at",
                "date_joined",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email_or_phone",
                "password1",
                "password2",
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")

    def get_queryset(self, request):
        """
        Show all users (including soft-deleted) in admin.
        """
        return User.objects.all()


