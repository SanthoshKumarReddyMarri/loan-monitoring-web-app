from rest_framework.views import APIView

from apps.core.responses import ApiResponse


class HealthCheckAPIView(APIView):
    """
    Simple endpoint to verify that the API is running.
    """

    def get(self, request):
        return ApiResponse.success(
            data={
                "status": "healthy",
            },
            message="API is running successfully.",
        )