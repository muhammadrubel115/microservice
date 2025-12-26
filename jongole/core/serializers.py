# jongole/core/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user_uuid', 'full_name', 'bio', 'created_at'] # Remove 'followers_count' from here