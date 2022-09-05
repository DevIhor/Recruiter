from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation endpoint."""

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Create and return a new user."""
        user = UserModel.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )
        return user

    class Meta:
        model = UserModel
        fields = ("email", "password")
