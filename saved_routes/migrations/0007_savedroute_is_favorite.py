# Generated by Django 4.2.7 on 2024-07-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saved_routes', '0006_savedroute_distance_savedroute_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedroute',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
