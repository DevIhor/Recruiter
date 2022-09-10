from apps.accounts.api.v1 import views
from django.urls import include, path

urlpatterns = [
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("email-confirm/<int:user_id>/<str:token>/", views.email_confirm, name="email_confirm"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
]
