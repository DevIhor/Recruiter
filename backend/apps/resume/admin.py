from django.contrib import admin
from apps.resume.models import CurriculumVitae


@admin.register(CurriculumVitae)
class CurriculumVitaeAdmin(admin.ModelAdmin):
    """This class registers Curriculum Vitae (CV) model at admin site."""

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
