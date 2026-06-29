from rest_framework import status
from rest_framework.response import Response

class ApiResponse:
    """
    Standard API response helper.
    """

    @staticmethod
    def success(
        data=None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        return Response(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=status_code,
        )

    @staticmethod
    def error(
        message: str = "Something went wrong.",
        errors=None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        return Response(
            {
                "success": False,
                "message": message,
                "errors": errors,
            },
            status=status_code,
        )