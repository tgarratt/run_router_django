from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    icon = models.IntegerField(blank=True, default=1)
    reset_token = models.CharField(max_length=255, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    # Add other custom fields as needed