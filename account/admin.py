from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProfileIcon

class CustomUserAdmin(UserAdmin):
    # Customize the admin panel as needed
     list_display = ['username', 'email', 'first_name', 'last_name', 'profile_icon', 'is_active', 'is_staff']

class IconAdmin(admin.ModelAdmin):
    # Customize the admin panel as needed
    list_display = ['id', 'source']

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(ProfileIcon, IconAdmin)
