import requests
from apps.accounts.api.v1.filters import UserFilter
from apps.accounts.api.v1.paginators import UserListPagination
from apps.accounts.api.v1.permissions import IsUserAccount
from apps.accounts.api.v1.serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserLoginSerializer,
    UserRetrieveUpdateDestroySerializer,
)
from apps.accounts.tasks import send_verification_email
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import F
from django.urls import reverse
from django_filters import rest_framework as django_filters
from rest_framework import filters, permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
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


class UserCreateAPIView(CreateAPIView):
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


class UserLoginAPIView(CreateAPIView):
    """View to login / obtain JWT token."""

    permissions = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Return JWT token if such user has already been registered.
        Send a confirmation email if account is inactive.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserModel.objects.filter(email=serializer.data.get("email")).first()
        # User does not exist
        if not user:
            return Response(
                {"detail": "Such user is not registered yet"}, status=status.HTTP_404_NOT_FOUND
            )
        # User is inactive
        if not user.is_active:
            send_verification_email.delay(user_id=user.id)  # run celery task to send an email
            return Response(
                {
                    "message": "You have not activated your account yet."
                    "Verification email has been sent to your email address. "
                    "Please check your inbox."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Obtain JWT token
        response = requests.post(
            url=request.build_absolute_uri(reverse("token_obtain_pair")), data=request.data
        )

        return Response(response.json(), status=status.HTTP_200_OK)


class UserListAPIView(ListAPIView):
    """
    LIST view for the User model.

    API
    ---
    get:
        Return a list of Users with the Profile data.

    """

    serializer_class = UserListSerializer
    pagination_class = UserListPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = UserFilter
    search_fields = ["=email", "user_profile__first_name", "user_profile__last_name"]
    ordering_fields = ["email", "first_name", "last_name"]
    ordering = ["first_name", "last_name"]

    def get_queryset(self):
        """
        Annotate a queryset to ba able to use user's `first_name` and `last_name`
        with `ordering` query parameter.
        """

        return (
            UserModel.objects.filter(is_active=True)
            .annotate(first_name=F("user_profile__first_name"))
            .annotate(last_name=F("user_profile__last_name"))
        )


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET / UPDATE / DELETE view for the User model.

    API
    ---
    get <id>:
        Return a User with its Profile info.

    put <id>:
        Update a User with its Profile info.

    patch <id>:
        Partially update a User with its Profile info.

    delete <id>:
        Deactivate the user account without complete deletion.

    """

    serializer_class = UserRetrieveUpdateDestroySerializer
    permission_classes = [permissions.IsAuthenticated, IsUserAccount]

    def get_queryset(self):
        return UserModel.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        """Get User by id."""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update User by id."""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Partially update User by id."""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Don't actually delete the user, set User account as inactive instead."""
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
