# Generated by Django 4.2.7 on 2024-07-08 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_rename_profileicons_profileicon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='profile_icon_id',
            new_name='profile_icon',
        ),
    ]
