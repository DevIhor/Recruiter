from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Currency, Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):

    """This class defines Vacancy model for use in admin panel."""

    list_display = (
        "title",
        "min_experience",
        "is_active",
        "search_period",
        "keyword_list",
        "type_of_employment",
        "english_level",
        "salary",
        "is_salary_show",
        "contact_person",
    )

    list_filter = ("is_salary_show", "type_of_employment", "english_level")

    search_fields = ("title",)

    fieldsets = (
        (
            _("Vacancy main info"),
            {
                "fields": (
                    "title",
                    "keywords",
                    "type_of_employment",
                    "location",
                    "english_level",
                    "min_experience",
                )
            },
        ),
        (_("Search period"), {"fields": ("start_date", "end_date")}),
        (_("Salary"), {"fields": ("salary_min", "salary_max", "salary_currency")}),
        (_("Other info"), {"fields": ("is_active", "is_salary_show")}),
        (_("Vacancy about info"), {"fields": ("description", "priority")}),
        (_("Contacts"), {"fields": ("contact_person", "author")}),
    )

    # required for correct display of tags
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("keywords")

    def keyword_list(self, obj):
        return ", ".join(o.name for o in obj.keywords.all())


admin.site.register(Currency)