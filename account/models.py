from django.db import models
from django.contrib.auth.models import AbstractUser

class ProfileIcon(models.Model):
    source = models.CharField(max_length=255)
    # Add other custom fields as needed

class CustomUser(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    profile_icon = models.ForeignKey(ProfileIcon, on_delete=models.SET_NULL, null=True)
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    # Add other custom fields as needed
