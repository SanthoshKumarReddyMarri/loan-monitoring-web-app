from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.serializers import (
    GoogleLoginSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import GoogleAuthService
from apps.core.responses import ApiResponse


class GoogleLoginAPIView(APIView):
    """
    Authenticate a user using Google OAuth.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = GoogleAuthService.authenticate(
            serializer.validated_data["id_token"]
        )

        user_data = UserResponseSerializer(result["user"]).data

        response= ApiResponse.success(
            data={
                # "access": result["tokens"]["access"],
                # "refresh": result["tokens"]["refresh"],
                "user": user_data,
            },
            message="Login successful.",
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie(
                    key="access_token",
                    value=result["tokens"]["access"],
                    httponly=True,
                    secure=False,
                    samesite="Lax",
                    path="/",
                )
                    
        return response
    

#check cookies functionality ,fetching user details
class MeAPIView(APIView):
    """
    Returns the currently authenticated user.
    """

    def get(self, request):

        user_data = UserResponseSerializer(request.user).data

        return ApiResponse.success(
            data=user_data,
            message="User fetched successfully.",
            status_code=status.HTTP_200_OK,
        )
        