# Generated by Django 4.2.7 on 2024-07-15 21:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saved_routes', '0002_rename_savedroute_savedroutes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SavedRoutes',
            new_name='SavedRoute',
        ),
    ]
