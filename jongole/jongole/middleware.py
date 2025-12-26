import requests
from django.conf import settings
from django.http import JsonResponse

class BrainlessAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.brainless_me_url = settings.BRAINLESS_BASE_URL + "/auth/me/"

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)

        token = auth_header.split(" ")[1]

        try:
            resp = requests.get(
                self.brainless_me_url,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5,
            )
        except requests.RequestException:
            return JsonResponse({"detail": "Authentication service unavailable."}, status=503)

        if resp.status_code != 200:
            return JsonResponse({"detail": "Invalid token or not authenticated."}, status=401)

        # Optionally attach user info to request
        request.user_info = resp.json()

        response = self.get_response(request)
        return response
