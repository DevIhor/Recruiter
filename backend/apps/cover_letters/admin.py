from django.contrib import admin
from apps.cover_letters.models import CoverLetter


@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    """This class registers CoverLetter model at admin site."""

    list_display = (
        "owner", 
        "file",
        "processed_by_tesseract", 
        "changed_at", 
        "cv_for_vacancies"
    )
    list_filter = (
        "owner", 
        "processed_by_tesseract"
    )
    list_per_page = 25
    search_fields = (
        "owner",
    )
    list_display_links = (
        "owner",
        "cv_for_vacancies",
    )
