# Generated by Django 5.0.1 on 2024-04-30 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialAPP', '0005_rename_image_profile_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='imagen',
        ),
    ]
