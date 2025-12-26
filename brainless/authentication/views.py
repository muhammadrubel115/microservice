from urllib import request
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
<<<<<<< HEAD
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken



=======
>>>>>>> 973a508fb6725d5c50031b2761615495605f5045

from .serializers import RegisterSerializer, LoginSerializer

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    refresh["user_uuid"] = str(user.user_uuid)
    refresh["role"] = user.role
    refresh["token_version"] = user.token_version
    refresh["is_active"] = user.is_active

    access = refresh.access_token
    access["user_uuid"] = str(user.user_uuid)
    access["role"] = user.role
    access["is_active"] = user.is_active

    return refresh



class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    http_method_names = ["post"]  # or ["get"]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "user_uuid": str(user.user_uuid),
                "email_or_phone": user.email_or_phone,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]  # or ["get"]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = generate_tokens(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

<<<<<<< HEAD
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken


from .permissions import IsTrustedService

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]  # include GET here

    def get(self, request):
        user = request.user

        if not user.is_active:
            return Response(
                {"detail": "Account inactive"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response({
            "user_uuid": str(user.user_uuid),
            "email_or_phone": user.email_or_phone,
            "username": user.username,
            "role": user.role,
        })



from .policies import get_permissions_for_role

class PermissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTrustedService]
    http_method_names = ["post"]  # or ["get"]

    def get(self, request):
        user = request.user

        perms = get_permissions_for_role(user.role)

        return Response({
            "user_uuid": str(user.user_uuid),
            "role": user.role,
            "permissions": list(perms),
        })
>>>>>>> 973a508fb6725d5c50031b2761615495605f5045

