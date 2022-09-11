from apps.accounts.models import Profile
from apps.events.models import Event, EventType
from rest_framework import serializers


class EventOwnerSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Profile model."""

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "avatar_image",
            "linkedin_url",
            "telegram_username",
        )


class EventTypeSerializer(serializers.ModelSerializer):
    """This is a serializer class for the EventType model."""

    class Meta:
        model = EventType
        fields = ("id", "title")


class EventListSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Event model."""

    owner_data = EventOwnerSerializer(source="owner", read_only=True)
    event_type_data = EventTypeSerializer(source="event_type", read_only=True)

    is_future = serializers.BooleanField(
        read_only=True,
    )
    visitors = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "event_type",
            "event_type_data",
            "priority",
            "owner",
            "owner_data",
            "start_time",
            "end_time",
            "duration",
            "created_at",
            "changed_at",
            "status",
            "visitors",
            "is_future",
        )
        read_only_fields = ("id", "owner", "created_at", "changed_at", "visitors", "is_future")


class EventRUDSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Event model."""

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "event_type",
            "priority",
            "owner",
            "start_time",
            "end_time",
            "duration",
            "created_at",
            "changed_at",
            "status",
        )
        read_only_fields = ("id", "owner", "created_at", "changed_at")
