from django.urls import path

from apps.accounts.views import (GoogleLoginAPIView,MeAPIView,)

urlpatterns = [
    path(
        "google/login/",
        GoogleLoginAPIView.as_view(),
        name="google-login",
    ),
    path("me/", MeAPIView.as_view(), name="me"),
]