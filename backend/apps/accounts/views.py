from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.accounts.serializers import (
    GoogleLoginSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import GoogleAuthService,AuthCookieService
from apps.core.responses import ApiResponse

from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


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

        AuthCookieService.set_access_cookie(
            response,
            result["tokens"]["access"],
        )

        AuthCookieService.set_refresh_cookie(
            response,
            result["tokens"]["refresh"],
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

        AuthCookieService.set_access_cookie(
            response,
            tokens["access"],
        )

        if "refresh" in tokens:
            AuthCookieService.set_refresh_cookie(
                response,
                tokens["refresh"],
            )

        return response
    

class LogoutAPIView(APIView):
    """
    Logout the user by blacklisting the refresh token
    and deleting authentication cookies.
    """

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass

        response = ApiResponse.success(
            message="Logout successful.",
            status_code=status.HTTP_200_OK,
        )

        AuthCookieService.clear_auth_cookies(response)

        return response
    


from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CSRFTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return ApiResponse.success(
            message="CSRF cookie set.",
            status_code=status.HTTP_200_OK,
        )