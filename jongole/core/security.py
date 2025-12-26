import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def verify_service_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.BRAINLESS_SECRET_KEY,
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Service token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid service token")

    if payload.get("type") != "service":
        raise AuthenticationFailed("Invalid token type")

    return payload
