from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreateForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    """This class defines User representation at AdminBoard."""

    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ("id", "email", "is_staff", "is_active")
    list_filter = ("is_staff",)
    fieldsets = (
        (_("Login info"), {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff")}),
    )
    add_fieldsets = (
        (_("Login info"), {"fields": ("email", "password1", "password2")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff")}),
    )
    search_fields = ("email",)
    ordering = ("id",)
