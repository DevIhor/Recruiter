from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.utils.translation import gettext_lazy as _
from apps.vacancies.models import Vacancy, Currency


class VacancySerializer(serializers.ModelSerializer, TaggitSerializer):
    """Serializer for CRUD Cacancy endpoint."""

    keywords = TagListSerializerField()
    end_date = serializers.DateField()
    start_date = serializers.DateField()
    salary_max = serializers.IntegerField()
    salary_min = serializers.IntegerField()

    class Meta:
        model = Vacancy
        fields = "__all__"

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(
                _("The end date must be after the start date!")
                )
        if data["salary_min"] > data["salary_max"]:
            raise serializers.ValidationError(
                _("The maximum salary must be greater than the minimum salary!")
                )
        return data


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for CRUD Currency endpoint."""

    class Meta:
        model = Currency
        fields = "__all__"
