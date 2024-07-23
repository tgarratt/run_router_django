from django.db import models
from account.models import CustomUser

class SavedRoute(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination_origin = models.CharField(max_length=255, blank=False, null=False, default="")
    destination_waypoint = models.CharField(max_length=255, blank=False, null=False, default="")
    distance = models.CharField(max_length=255, blank=False, null=False, default="")
    name = models.CharField(max_length=255, blank=False, null=False, default="")
    description = models.CharField(max_length=100, blank=True, null=True)
    is_favorite = models.BooleanField(default=False)
    # Add other custom fields as needed