# Generated by Django 3.2.12 on 2022-10-03 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_posts_draft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='draft',
        ),
    ]
