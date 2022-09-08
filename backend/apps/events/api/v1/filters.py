from apps.events.models import Event
from django_filters import rest_framework as filters


class EventFilter(filters.FilterSet):
    """This is a filter settings for the Event model."""

    title = filters.CharFilter(lookup_expr="icontains")
    min_priority = filters.NumberFilter(field_name="priority", lookup_expr="gte")
    max_priority = filters.NumberFilter(field_name="priority", lookup_expr="lte")
    min_visitors = filters.NumberFilter(field_name="visitors", lookup_expr="gte")
    max_visitors = filters.NumberFilter(field_name="visitors", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ("created_at", "start_time", "end_time", "duration")
