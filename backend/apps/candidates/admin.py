from django.contrib import admin
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _
from .models import Candidate
from .widgets import DateSelectorWidget


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """This class defines Candinate model for use in admin panel."""
    list_display = ("full_name", "age", "phone_number", "email", "level_of_english")
    list_per_page = 25
    formfield_overrides = {
        DateField: {"widget": DateSelectorWidget},
    }
    search_fields = ("name", "surname", "email", "phone_number")
    fieldsets = (
        (_("Personal info"), {"fields": ("name", "surname", "date_of_birth", "gender")}),
        (_("Contact info"), {"fields": ("phone_number", "email", "additional_contacts")}),
        (_("Qualities"), {"fields": ("level_of_english", "notes")}),
    )
    add_fieldsets = (
        (_("Personal info"), {"fields": ("name", "surname", "date_of_birth", "gender")}),
        (_("Contact info"), {"fields": ("phone_number", "email")}),
    )
