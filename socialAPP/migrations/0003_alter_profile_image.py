# Generated by Django 5.0.1 on 2024-04-30 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialAPP', '0002_remove_userprofile_user_post_profile_relationship_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='imagenes'),
        ),
    ]
