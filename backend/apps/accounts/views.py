from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.serializers import (
    GoogleLoginSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import GoogleAuthService
from apps.core.responses import ApiResponse

from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class GoogleLoginAPIView(APIView):
    """
    Authenticate a user using Google OAuth.
    """

    #this will resolve many issues ,it wont check any access tokens prev exist or not and will allow any user to access this endpoint
    authentication_classes = []
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
        
        response.set_cookie(
                    key="refresh_token",
                    value=result["tokens"]["refresh"],
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
    



#Handling token refresh using cookies
class TokenRefreshAPIView(APIView):
    """
    Refresh the access token using the refresh token
    stored in an HttpOnly cookie.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return ApiResponse.error(
                message="Refresh token not found.",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(
            data={"refresh": refresh_token}
        )

        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data

        response = ApiResponse.success(
            message="Token refreshed successfully.",
            status_code=status.HTTP_200_OK,
        )

        # New access token
        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
        )

        # Because ROTATE_REFRESH_TOKENS=True,
        # SimpleJWT can return a new refresh token too.
        if "refresh" in tokens:
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,
                samesite="Lax",
                path="/",
            )

        return response