from apps.candidates.models import Candidate
from base.widgets import DateSelectorWidget
from django.contrib import admin
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportMixin


class CandidateResource(resources.ModelResource):
    """This allows users to export/import Candidates."""

    class Meta:
        model = Candidate
        skip_unchanged = True
        report_skipped = True


@admin.register(Candidate)
class CandidateAdmin(ImportExportMixin, admin.ModelAdmin):
    """This class defines Candidate model for use in admin panel."""

    resource_class = CandidateResource
    list_display = (
        "full_name",
        "age",
        "phone_number",
        "email",
        "level_of_english",
        "applications_for_vacancies",
    )
    list_display_links = (
        "full_name",
        "applications_for_vacancies",
    )
    list_per_page = 25
    formfield_overrides = {
        DateField: {"widget": DateSelectorWidget},
    }
    search_fields = ("name", "surname", "email", "phone_number")
    fieldsets = (
        (_("Personal info"), {"fields": ("name", "surname", "date_of_birth", "gender")}),
        (_("Contact info"), {"fields": ("phone_number", "email", "additional_contacts")}),
        (_("Qualities"), {"fields": ("level_of_english", "notes")}),
        (_("Vacancies"), {"fields": ("vacancy",)}),
    )
    add_fieldsets = (
        (_("Personal info"), {"fields": ("name", "surname", "date_of_birth", "gender")}),
        (_("Contact info"), {"fields": ("phone_number", "email")}),
    )

    list_filter = (
        "level_of_english",
        "vacancy",
    )
