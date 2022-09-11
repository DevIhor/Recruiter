from apps.candidates.models import Candidate
from django_filters import rest_framework as filters


class CandidateFilter(filters.FilterSet):
    """This is a filter settings for the Candidate model."""

    fullname = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Candidate
        fields = ("created_at",)
