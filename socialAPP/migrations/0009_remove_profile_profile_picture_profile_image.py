# Generated by Django 5.0.1 on 2024-05-14 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialAPP', '0008_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='batman.png', upload_to=''),
        ),
    ]
