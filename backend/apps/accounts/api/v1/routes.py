from apps.accounts.api.v1 import views
from django.urls import path

urlpatterns = [
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("email-confirm/<int:user_id>/<str:token>/", views.email_confirm, name="email_confirm"),
    path("login/", views.UserLoginView.as_view(), name="login"),
]
