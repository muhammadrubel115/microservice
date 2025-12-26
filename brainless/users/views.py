from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return the authenticated user's safe data.
        UUID-based authentication ensures request.user is valid.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
