from django.urls import path

from apps.accounts.views import (GoogleLoginAPIView,MeAPIView,TokenRefreshAPIView,)

urlpatterns = [
    path(
        "google/login/",
        GoogleLoginAPIView.as_view(),
        name="google-login",
    ),
    path("me/", MeAPIView.as_view(), name="me"),

    path("refresh/", TokenRefreshAPIView.as_view(), name="token-refresh"),
]