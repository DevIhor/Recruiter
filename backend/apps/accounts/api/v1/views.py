from apps.accounts.api.v1.serializers import UserCreateSerializer
from apps.accounts.tasks import send_verification_email
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

UserModel = get_user_model()


@api_view(["GET"])
def email_confirm(request, user_id: int, token: str):
    """View to activate user's account by clicking on activation link."""

    user = UserModel.objects.filter(id=user_id).first()
    if user is None:
        return Response({"detail": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response(
            {
                "detail": "Token is invalid or expired. "
                "Please request another confirmation email by signing in."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.is_active = True
    user.save()
    return Response({"message": "Email address successfully confirmed"}, status.HTTP_200_OK)


class UserCreateView(CreateAPIView):
    """View for creating a new user."""

    model = UserModel
    permissions = [permissions.AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new user with the provided email and password.
        Send the verification email with an activation link.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_verification_email.delay(user_id=user.id)  # initiate celery task to send an email

        return Response(
            {
                "message": "Verification email has been sent to your email address. "
                "Please check your inbox."
            },
            status=status.HTTP_201_CREATED,
        )
