from apps.accounts.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user creation endpoint."""

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Create a new user and a new profile for this user. Return user."""

        user = UserModel.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
        )

        Profile.objects.create(
            user=user,
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
        )

        return user

    class Meta:
        model = UserModel
        fields = ("first_name", "last_name", "email", "password")


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login api endpoint."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("email", "password")


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "address",
            "phone_number",
            "avatar_image",
            "linkedin_url",
            "telegram_username",
            "additional_info",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for the user list api endpoint."""

    profile_info = ProfileSerializer(source="user_profile")

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "profile_info",
        )


class UserRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    """Serializer for the user detail api endpoint."""

    profile_info = ProfileSerializer(source="user_profile")

    class Meta:
        model = UserModel
        fields = (
            "id",
            "email",
            "profile_info",
        )
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        """Update user instance and its profile info. Return user."""

        # update profile
        profile_data = validated_data.pop("user_profile")
        for k, v in profile_data.items():
            setattr(instance.user_profile, k, v)
        instance.user_profile.save()

        # update user
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance
