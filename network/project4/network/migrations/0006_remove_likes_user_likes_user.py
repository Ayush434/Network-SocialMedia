# Generated by Django 4.0.6 on 2022-12-02 03:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_likes_post_likes_postid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='user',
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ManyToManyField(blank=True, max_length=50, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
