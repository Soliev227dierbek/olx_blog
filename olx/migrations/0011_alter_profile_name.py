# Generated by Django 5.1.6 on 2025-04-02 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olx', '0010_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
    ]
