# Generated by Django 4.2.7 on 2024-07-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saved_routes', '0007_savedroute_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedroute',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='savedroute',
            name='destination_origin',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='savedroute',
            name='destination_waypoint',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='savedroute',
            name='distance',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='savedroute',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
