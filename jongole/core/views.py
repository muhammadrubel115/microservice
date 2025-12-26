# jongole/core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user is a 'TokenUser' object because of our stateless settings.
        # We access the 'user_uuid' claim directly from the token.
        user_uuid = request.user.token.get('user_uuid')
        
        # Get or create profile for this specific UUID
        profile, created = Profile.objects.get_or_create(user_uuid=user_uuid)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        user_uuid = request.user.token.get('user_uuid')
        profile = Profile.objects.get(user_uuid=user_uuid)
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)