from django.shortcuts import render

# Create your views here.
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Service
from datetime import datetime, timedelta


class ServiceAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        name = request.data.get("service_name")
        secret = request.data.get("secret")

        try:
            service = Service.objects.get(name=name, is_active=True)
        except Service.DoesNotExist:
            return Response({"detail": "Invalid service"}, status=401)

        if service.secret != secret:
            return Response({"detail": "Unauthorized"}, status=401)

        payload = {
            "service": service.name,
            "type": "service",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=30),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"access": token})
