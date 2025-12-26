from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Only expose safe fields
        fields = (
            "user_uuid",      # Always UUID
            "email_or_phone",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role",
            "is_email_verified",
            "is_phone_verified",
        )
        read_only_fields = (
            "user_uuid",
            "role",
            "is_email_verified",
            "is_phone_verified",
        )
