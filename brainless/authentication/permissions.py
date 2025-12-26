import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission


class IsTrustedService(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("X-Service-Token")
        if not token:
            return False

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.InvalidTokenError:
            return False

        return payload.get("type") == "service"
