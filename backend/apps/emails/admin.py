from apps.emails.tasks import send_emails
from apps.emails.forms import HTMLTextField
from apps.emails.models import EmailLetter, EmailTemplate
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description="Send emails")
def send_emails_admin(self, request, queryset):
    for email in queryset:
        send_emails.delay(email_letter=email)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """This class defines EmailTemplate representation at Admin site."""

    list_per_page = 25
    list_display = ("name", "description", "author", "created_at")
    search_fields = ("name", "description")

    fieldsets = (
        (_("General info"), {"fields": ("name", "description", "author")}),
        (_("Email"), {"fields": ("subject", "body")}),
    )

    form = HTMLTextField


@admin.register(EmailLetter)
class EmailLetterAdmin(admin.ModelAdmin):
    """This class defines EmailLetter representation at Admin site."""

    list_per_page = 25
    list_display = ("name", "created_at", "status", "sent_time")
    search_fields = ("name", "template")
    actions = (send_emails_admin,)
    fieldsets = (
        (_("General info"), {"fields": ("name", "template")}),
        (_("Extra info"), {"fields": ("vacancy", "event")}),
        (_("Recipients"), {"fields": ("recipients",)}),
    )
