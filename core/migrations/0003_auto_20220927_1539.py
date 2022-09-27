# Generated by Django 3.2.12 on 2022-09-27 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_posts_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='comment_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='posts',
            name='like_count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='posts',
            name='save_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
