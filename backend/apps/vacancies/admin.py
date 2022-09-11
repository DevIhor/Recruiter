from apps.vacancies.models import Currency, Vacancy
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportMixin


@admin.action(description="Mark selected vacancies as active")
def activate(self, request, queryset):
    for vacancy in queryset:
        vacancy.is_active = True
        vacancy.save()


@admin.action(description="Mark selected vacancies as inactive")
def deactivate(self, request, queryset):
    for vacancy in queryset:
        vacancy.is_active = False
        vacancy.save()


@admin.action(description="Show salary in selected vacancies")
def salary_show(self, request, queryset):
    for vacancy in queryset:
        vacancy.is_salary_show = True
        vacancy.save()


@admin.action(description="Don't show salary in selected vacancies")
def salary_dont_show(self, request, queryset):
    for vacancy in queryset:
        vacancy.is_salary_show = False
        vacancy.save()


class VacancyResource(resources.ModelResource):
    """This allows users to export/import Vacancies."""

    class Meta:
        model = Vacancy
        skip_unchanged = True
        report_skipped = True


@admin.register(Vacancy)
class VacancyAdmin(ImportExportMixin, admin.ModelAdmin):
    """This class defines Vacancy model for use in admin panel."""

    resource_class = VacancyResource

    actions = (activate, deactivate, salary_show, salary_dont_show)

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

    list_filter = (
        "is_salary_show", 
        "type_of_employment", 
        "english_level",
        "is_active"
    )

    search_fields = ("title",)

    fieldsets = (
        (_("Vacancy main info"),{"fields": (
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
