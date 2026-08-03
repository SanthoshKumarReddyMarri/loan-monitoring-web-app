from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        access_token = request.COOKIES.get(settings.AUTH_COOKIE_ACCESS_NAME)

        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)
        user = self.get_user(validated_token)

        self.enforce_csrf(request)

        return user, validated_token

    def enforce_csrf(self, request):
        check = CSRFCheck(lambda req: None)

        check.process_request(request)

        reason = check.process_view(
            request,
            None,
            (),
            {},
        )

        if reason:
            raise PermissionDenied(
                f"CSRF Failed: {reason}"
            )