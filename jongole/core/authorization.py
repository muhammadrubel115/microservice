import requests
from django.conf import settings
from rest_framework.exceptions import PermissionDenied


def fetch_user_permissions(user_token, service_token):
    headers = {
        "Authorization": f"Bearer {user_token}",
        "X-Service-Token": service_token,
    }

    r = requests.get(
        f"{settings.BRAINLESS_BASE_URL}/api/auth/permissions/",
        headers=headers,
        timeout=3,
    )

    if r.status_code != 200:
        raise PermissionDenied("Permission check failed")

    return r.json()["permissions"]
