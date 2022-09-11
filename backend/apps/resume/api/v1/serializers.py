from apps.candidates.models import Candidate
from apps.resume.models import CurriculumVitae
from rest_framework import serializers


class CVOwnerSerializer(serializers.ModelSerializer):
    """This is a serializer class for the Profile model."""

    class Meta:
        model = Candidate
        fields = (
            "name",
            "surname",
            "phone_number",
            "email",
        )


class CurriculumVitaeListSerializer(serializers.ModelSerializer):
    """This is a serializer class for the CurriculumVitae model."""

    candidate_data = CVOwnerSerializer(source="owner", read_only=True)

    class Meta:
        model = CurriculumVitae
        fields = (
            "id",
            "owner",
            "vacancy",
            "file",
            "content",
            "processed_by_tesseract",
            "created_at",
            "changed_at",
            "candidate_data",
        )
        read_only_fields = ("id", "created_at", "changed_at", "candidate_data")


class CurriculumVitaeRUDSerializer(serializers.ModelSerializer):
    """This is a serializer class for the CurriculumVitae model."""

    class Meta:
        model = CurriculumVitae
        fields = (
            "id",
            "owner",
            "vacancy",
            "file",
            "content",
            "processed_by_tesseract",
            "created_at",
            "changed_at",
        )
        read_only_fields = ("id", "owner", "vacancy", "created_at", "changed_at")
