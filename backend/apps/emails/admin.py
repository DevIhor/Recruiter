from apps.emails.forms import HTMLTextField
from apps.emails.models import EmailTemplate
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """This class defines EmailTemplate representation at Admin site."""

    list_per_page = 25
    list_display = ("name", "description", "created_at")
    search_fields = ("name", "description")

    fieldsets = (
        (_("General info"), {"fields": ("name", "description")}),
        (_("Email"), {"fields": ("subject", "body")}),
    )

    form = HTMLTextField
