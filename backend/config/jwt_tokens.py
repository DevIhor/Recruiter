from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

jwt_token_obtain = path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair")
jwt_token_refresh = path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
