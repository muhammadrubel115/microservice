from django.db import models

# Create your only User  models here.


# write your imports here !!!

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from users.validators import email_or_phone_validator
from django.utils import timezone
from django.conf import settings
from django.db import models

import uuid

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email_or_phone, password=None, role="user", **extra_fields):
        if not email_or_phone:
            raise ValueError("Users must have an email or phone number")

        user = self.model(
            email_or_phone=email_or_phone,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_or_phone, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email_or_phone, password, **extra_fields)



class ActiveUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class User(AbstractBaseUser, PermissionsMixin):
    user_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
        ("role1", "Role1"),
        
    )

    # Core identity (login field)
    email_or_phone = models.CharField(
        max_length=100,
        unique=True,
        validators=[email_or_phone_validator],
    )

    # Optional profile fields
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    
    email = models.EmailField(max_length=150, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    phone = models.CharField(max_length=20, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)


    token_version = models.PositiveIntegerField(default=1)

    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)



    
    # Role & permissions
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="users",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="users",
        blank=True,
    )


    objects = UserManager()
    active = ActiveUserManager()


    USERNAME_FIELD = "email_or_phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email_or_phone
    
    class Meta:
        indexes = [
            models.Index(fields=["email_or_phone"]),
            models.Index(fields=["role"]),
        ]

    # Helpers
    @property
    def is_email(self):
        return "@" in self.email_or_phone
    @property
    def is_phone(self):
        return self.email_or_phone.isdigit()
    
    @property
    def is_authenticated_active(self):
        return self.is_active and not self.is_deleted

    def save(self, *args, **kwargs):
        if self.email_or_phone:
            value = self.email_or_phone.strip().lower()
            self.email_or_phone = value

            if "@" in value:
                self.email = self.email or value
            elif value.isdigit():
                self.phone = self.phone or value

        super().save(*args, **kwargs)




# users/models.py

import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class VerificationCode(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=6)  # 6 digit code
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.expires_at is None:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        else:
            self.expires_at = self.expires_at + timedelta(minutes=10)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.email_or_phone} - {self.code} - Used: {self.is_used}"
