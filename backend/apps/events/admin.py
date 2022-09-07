from apps.events.models import Event, EventType
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.action(description="Mark selected events as completed")
def make_completed(self, request, queryset):
    for event in queryset:
        event.mark_as_completed()
        event.save()


@admin.action(description="Mark selected events as cancelled")
def make_cancelled(self, request, queryset):
    for event in queryset:
        event.mark_as_cancelled()
        event.save()


@admin.action(description="Mark selected events as active")
def make_active(self, request, queryset):
    for event in queryset:
        event.mark_as_active()
        event.save()


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    """This class registers EventType model at admin site."""

    list_display = ("id", "title")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """This class registers Event model at admin site."""

    actions = (make_completed, make_active, make_cancelled)

    list_display = ("title", "event_type", "status", "priority", "start_time", "duration", "owner")
    list_filter = ("duration", "owner", "event_type", "priority")
    list_per_page = 25

    search_fields = (
        "title",
        "event_type",
        "owner",
    )

    fieldsets = (
        (_("Information"), {"fields": ("title", "description", "event_type", "priority", "owner")}),
        (_("Time info"), {"fields": ("start_time", "end_time")}),
        (_("Participants"), {"fields": ("staff_participants", "candidate_participants")}),
    )
