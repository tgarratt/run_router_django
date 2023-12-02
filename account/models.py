from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    icon = models.IntegerField(blank=True, default=1)
    # Add other custom fields as needed