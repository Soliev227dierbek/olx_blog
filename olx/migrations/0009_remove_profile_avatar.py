# Generated by Django 5.1.6 on 2025-04-01 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0008_profile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
    ]
