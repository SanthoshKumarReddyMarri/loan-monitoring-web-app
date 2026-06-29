from django.urls import path

from apps.health.views import HealthCheckAPIView

urlpatterns = [
    path("", HealthCheckAPIView.as_view(), name="health-check"),
]