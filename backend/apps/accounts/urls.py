from django.urls import path

from apps.accounts.views import (GoogleLoginAPIView,MeAPIView,TokenRefreshAPIView,LogoutAPIView,CSRFTokenAPIView)

urlpatterns = [
    path(
        "google/login/",
        GoogleLoginAPIView.as_view(),
        name="google-login",
    ),
    path("me/", MeAPIView.as_view(), name="me"),

    path("refresh/", TokenRefreshAPIView.as_view(), name="token-refresh"),

    path("logout/", LogoutAPIView.as_view(), name="logout"),

    path("csrf/",CSRFTokenAPIView.as_view(),name="csrf-token",),
]