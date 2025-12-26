# brainless/views.py
from rest_framework_simplejwt.tokens import RefreshToken

def issue_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

import requests

def verify_user(token):
    response = requests.get(
        "http://user-service/auth/verify/",
        headers={"Authorization": f"Bearer {token}"}
    )
    response.raise_for_status()
    return response.json()

def process_logic(request):
    token = request.headers.get("Authorization", "").split(" ")[1]
    user = verify_user(token)

    # user contains id, role, permissions
    result = execute_business_logic(user)
    return JsonResponse(result)

def calculate_discount(user, cart):
    if user["role"] == "premium":
        return 20
    return 5
