from django.db import models

class Profile(models.Model):
    # This UUID comes from the Brainless JWT
    user_uuid = models.UUIDField(primary_key=True, editable=False)
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user_uuid}"