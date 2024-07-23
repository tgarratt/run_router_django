from django.contrib import admin
from .models import SavedRoute

class SavedRouteAdmin(admin.ModelAdmin):
    # Customize the admin panel as needed
     list_display = ['destination_origin', 'destination_waypoint', 'user']


admin.site.register(SavedRoute, SavedRouteAdmin)
