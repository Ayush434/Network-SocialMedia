# Generated by Django 4.0.6 on 2022-12-02 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_likes_like_remove_likes_postid_likes_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='num_of_likes',
            field=models.IntegerField(default='0'),
        ),
    ]
