# Generated by Django 4.2.7 on 2024-07-15 21:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('saved_routes', '0003_rename_savedroutes_savedroute'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedRoutes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination_origin', models.CharField(blank=True, max_length=255, null=True)),
                ('destination_waypoint', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='SavedRoute',
        ),
    ]
