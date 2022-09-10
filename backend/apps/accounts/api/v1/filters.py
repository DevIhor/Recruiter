import django_filters
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        field_name="user_profile__first_name", lookup_expr="icontains"
    )
    last_name = django_filters.CharFilter(
        field_name="user_profile__last_name", lookup_expr="icontains"
    )

    class Meta:
        model = UserModel
        fields = ["email", "first_name", "last_name"]
