from google.auth.transport import requests
from google.oauth2 import id_token

from django.conf import settings

from django.contrib.auth import get_user_model

import uuid

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class GoogleAuthService:
    """
    Handles Google OAuth authentication.
    """

    @staticmethod
    def verify_google_token(token: str):
        """
        Verify the Google ID token.
        """

        return id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    
    @staticmethod
    def get_or_create_user(google_user_data: dict):
        """
        Retrieve an existing user or create a new one from
        verified Google user information.
        """

        email = google_user_data["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": GoogleAuthService.generate_username(email),
                "first_name": google_user_data.get("given_name", ""),
                "last_name": google_user_data.get("family_name", ""),
                "google_id": google_user_data.get("sub"),
                "profile_picture": google_user_data.get("picture", ""),
            },
        )

        if not created:
            user.google_id = google_user_data.get("sub")
            user.profile_picture = google_user_data.get("picture", "")
            user.first_name = google_user_data.get("given_name", "")
            user.last_name = google_user_data.get("family_name", "")
            user.save(
                update_fields=[
                    "google_id",
                    "profile_picture",
                    "first_name",
                    "last_name",
                    "updated_at",
                ]
            )

        return user
    
    import uuid


@staticmethod
def generate_username(email: str) -> str:
    """
    Generate a unique username from the email address.
    """

    prefix = email.split("@")[0]
    suffix = uuid.uuid4().hex[:8]

    return f"{prefix}_{suffix}"


@staticmethod
def generate_tokens(user):
    """
    Generate JWT access and refresh tokens.
    """

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@staticmethod
def authenticate(id_token: str):
    """
    Authenticate a user using a Google ID token.
    """

    google_user = GoogleAuthService.verify_google_token(id_token)

    user = GoogleAuthService.get_or_create_user(google_user)

    tokens = GoogleAuthService.generate_tokens(user)

    return {
        "user": user,
        "tokens": tokens,
    }