# Generated by Django 3.2.12 on 2022-10-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_comments_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
