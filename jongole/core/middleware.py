from urllib import request
from django.utils.deprecation import MiddlewareMixin
from .security import verify_service_token


class ServiceAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.headers.get("Authorization")
        if not auth:
            return

        token = auth.replace("Bearer ", "")
        request.service = verify_service_token(token)

from .brainless import fetch_user_identity
from rest_framework.exceptions import AuthenticationFailed
from .authorization import fetch_user_permissions

class UserContextMiddleware:
    
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_token = request.headers.get("Authorization")
        service_token = request.headers.get("X-Service-Token")

        if user_token and service_token:
            user_token = user_token.replace("Bearer ", "")
            request.user_context = fetch_user_identity(
                user_token,
                service_token,
            )
            request.permissions = fetch_user_permissions(user_token, service_token)
        else:
            request.user_context = None

        return self.get_response(request)
