from base.widgets import DateSelectorWidget
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreateForm
from .models import Profile


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """A class to represent the user's Profile at admin panel."""

    list_display = ("full_name", "age", "get_email", "phone_number", "days_on_site")
    list_per_page = 25
    formfield_overrides = {
        DateField: {"widget": DateSelectorWidget},
    }
    search_fields = ("user__email", "first_name", "last_name")
    fieldsets = (
        (_("User instance"), {"fields": ("user",)}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "date_of_birth", "gender", "address")},
        ),
        (_("Contact info"), {"fields": ("phone_number", "linkedin_url", "telegram_username")}),
        (_("Additional info"), {"fields": ("avatar_image", "additional_info")}),
    )
    raw_id_fields = ("user",)
    list_select_related = ("user",)

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email address"
