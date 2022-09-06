from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login endpoint."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("email", "password")
