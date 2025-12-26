from rest_framework import serializers
from django.utils import timezone
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ❌ REMOVE user_id explicitly
        token.pop("user_id", None)

        # ✅ UUID as identity
        token["user_uuid"] = str(user.user_uuid)

        # Optional custom claims
        token["role"] = user.role
        token["token_version"] = user.token_version
        token["is_active"] = user.is_active

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "email_or_phone",
            "password",
            "first_name",
            "last_name",
            "username",
            "role",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    serializer_class = CustomTokenObtainPairSerializer
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(
                email_or_phone=attrs["email_or_phone"],
                is_deleted=False,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Account locked check
        if user.locked_until and user.locked_until > timezone.now():
            raise serializers.ValidationError("Account is temporarily locked")

        if not user.check_password(attrs["password"]):
            user.failed_login_attempts += 1
            user.save(update_fields=["failed_login_attempts"])
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")

        # Reset failed attempts
        user.failed_login_attempts = 0
        user.last_login_at = timezone.now()
        user.save(update_fields=["failed_login_attempts", "last_login_at"])

        attrs["user"] = user
        return attrs

