# Generated by Django 3.2.12 on 2022-09-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
