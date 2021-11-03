from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions

def enforce_csrf(request):
    check = CSRFCheck()

    check.process_request(request)

    reason = check.process_view(request, None, (), {})

    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['JWT_COOKIE_NAME']) or None
        else:
            raw_token = self.get_raw_token(header)

        if not raw_token:
            return None

        validated_token = self.get_validated_token(raw_token)
        # enforce_csrf(request)

        return self.get_user(validated_token), validated_token

