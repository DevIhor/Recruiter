from apps.accounts.forms import UserChangeForm, UserCreateForm
from apps.accounts.models import Profile
from base.widgets import DateSelectorWidget
from django.contrib import admin
from django.contrib.auth import get_user_model, models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _
from import_export import fields, resources
from import_export.admin import ImportExportMixin
from import_export.widgets import ForeignKeyWidget

USER_MODEL = get_user_model()


class UsersResource(resources.ModelResource):
    """This allows users to export/import Users."""

    class Meta:
        model = USER_MODEL
        skip_unchanged = True
        report_skipped = True


class ProfileResource(resources.ModelResource):
    """This allows users to export/import Profiles."""

    class Meta:

        user = fields.Field(
            column_name="user",
            attribute="user",
            widget=ForeignKeyWidget(USER_MODEL),
        )

        model = Profile
        fields = (
            "additional_info",
            "address",
            "avatar_image",
            "created_at",
            "date_of_birth",
            "first_name",
            "gender",
            "id",
            "last_name",
            "linkedin_url",
            "phone_number",
            "telegram_username",
            "updated_at",
            "user",
            "user__email",
            "user__is_active",
            "user__is_staff",
            "user__is_superuser",
            "user_password",
        )
        skip_unchanged = False
        report_skipped = False


@admin.action(description="Add to Recruiters")
def put_to_recruiters(self, request, queryset):
    group = models.Group.objects.get(name="Recruiter")
    for user in queryset:
        if not user.has_group("Recruiter"):
            user.groups.add(group)


@admin.action(description="Add to Reviewers")
def put_to_reviewers(self, request, queryset):
    group = models.Group.objects.get(name="Reviewer")
    for user in queryset:
        if not user.has_group("Reviewer"):
            user.groups.add(group)


class CustomUserInline(admin.TabularInline):
    """Class allows to add CustomUser in Group admin page."""

    model = USER_MODEL.groups.through
    extra = 1


@admin.register(USER_MODEL)
class UserAdmin(ImportExportMixin, BaseUserAdmin):
    """This class defines User representation at AdminBoard."""

    resource_class = UsersResource

    actions = (
        put_to_recruiters,
        put_to_reviewers,
    )

    inlines = (CustomUserInline,)
    form = UserChangeForm
    add_form = UserCreateForm
    list_display = ("id", "email", "is_staff", "is_active", "user_groups")
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
class ProfileAdmin(ImportExportMixin, admin.ModelAdmin):
    """A class to represent the user's Profile at admin panel."""

    resource_class = ProfileResource

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
