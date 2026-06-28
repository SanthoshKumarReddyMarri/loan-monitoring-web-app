from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


'''
Abstarct user deafult takes the belon values
username
password
first_name
last_name
email
groups
permissions
is_staff
is_superuser
last_login
date_joined
'''

class User(TimeStampedModel, AbstractUser):
    """
    Custom user model for the Loan Monitoring application.
    Supports Google OAuth authentication while remaining
    compatible with Django's authentication system.
    
    """

    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="Unique email address used for authentication.",
    )

    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text="Unique Google account identifier.",
    )

    profile_picture = models.URLField(
        max_length=500,
        blank=True,
        help_text="Google profile picture URL.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.email