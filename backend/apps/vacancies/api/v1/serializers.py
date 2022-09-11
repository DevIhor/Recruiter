from apps.vacancies.models import Currency, Vacancy
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField


class UserSerializer(serializers.ModelSerializer):
    """This is a serializer class for the User model."""
    class Meta:

        model = User
        fields = ("email",)


class VacancySerializer(serializers.ModelSerializer, TaggitSerializer):
    """Serializer for CRUD Vacancy endpoint."""

    keywords = TagListSerializerField()

    author_data = UserSerializer(source="author", read_only=True)
    contact_person_data = UserSerializer(source="contact_person", read_only=True)

    class Meta:
        model = Vacancy
        fields = (
            "id", 
            "title",
            "keywords",
            "type_of_employment",
            "location",
            "english_level",
            "min_experience",
            "end_date",
            "start_date",
            "description",
            "priority",
            "salary_max",
            "salary_min",
            "salary_currency",
            "is_active",
            "is_salary_show",
            "author_data",
            "contact_person_data"
        )

    def validate(self, data):
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError(_("The end date must be after the start date!"))
        if data["salary_min"] > data["salary_max"]:
            raise serializers.ValidationError(
                _("The maximum salary must be greater than the minimum salary!")
            )
        return data


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for CRUD Currency endpoint."""

    class Meta:
        model = Currency
        fields = ("id", "currency_title", "currency_code")
