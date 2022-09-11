from apps.candidates.models import Candidate
from rest_framework import serializers


class CandidateListSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Event model."""

    vacancies_count = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Candidate
        fields = (
            "id",
            "name",
            "surname",
            "date_of_birth",
            "gender",
            "phone_number",
            "email",
            "level_of_english",
            "notes",
            "additional_contacts",
            "created_at",
            "updated_at",
            "vacancies_count",
        )
        read_only_fields = ("id", "created_at", "updated_at", "vacancies_count", "age")


class CandidateRUDSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Event model."""

    class Meta:
        model = Candidate
        fields = (
            "id",
            "name",
            "surname",
            "date_of_birth",
            "gender",
            "phone_number",
            "email",
            "level_of_english",
            "notes",
            "additional_contacts",
            "updated_at",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "age")
