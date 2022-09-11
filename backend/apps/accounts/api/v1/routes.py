from apps.accounts.api.v1 import views
from django.urls import include, path

urlpatterns = [
    # AUTH
    path("signup/", views.UserCreateAPIView.as_view(), name="signup"),
    path("email-confirm/<int:user_id>/<str:token>/", views.email_confirm, name="email_confirm"),
    path("login/", views.UserLoginAPIView.as_view(), name="login"),
    path("password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    # USER CRUD
    path("users/", views.UserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user_detail"),
]
