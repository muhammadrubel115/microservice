from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_deleted or not user.is_active:
            return Response(
                {"detail": "Account inactive"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response({
            "user_uuid": str(user.user_uuid),
            "email_or_phone": user.email_or_phone,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        })
