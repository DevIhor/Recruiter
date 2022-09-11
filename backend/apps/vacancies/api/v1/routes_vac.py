from apps.vacancies.api.v1 import views
from django.urls import path

urlpatterns = [
    path("", views.VacancyListViewSet.as_view(), name="vacancies"),
    path("<int:pk>", views.VacancyViewSet.as_view(), name="vacancy")
]
