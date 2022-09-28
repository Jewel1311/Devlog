# Generated by Django 3.2.12 on 2022-09-28 14:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='connections',
            field=models.ManyToManyField(related_name='connections', to=settings.AUTH_USER_MODEL),
        ),
    ]
