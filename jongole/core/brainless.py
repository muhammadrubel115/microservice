import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def fetch_user_identity(user_token, service_token):
    headers = {
        "Authorization": f"Bearer {user_token}",
        "X-Service-Token": service_token,
    }

    response = requests.get(
        f"{settings.BRAINLESS_BASE_URL}/api/auth/me/",
        headers=headers,
        timeout=3,
    )

    if response.status_code != 200:
        raise AuthenticationFailed("User identity verification failed")

    return response.json()
