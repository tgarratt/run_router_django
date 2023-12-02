from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Customize the admin panel as needed
     list_display = ['username', 'email', 'first_name', 'last_name', 'icon', 'is_active', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
