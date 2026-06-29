from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginSerializer(serializers.Serializer):
    """
    Validate Google OAuth login request.
    """

    id_token = serializers.CharField(
        required=True,
        allow_blank=False,
        help_text="Google ID token returned by Google Sign-In.",
    )


class UserResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for authenticated user details.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
        )