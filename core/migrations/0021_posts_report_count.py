# Generated by Django 3.2.12 on 2023-03-18 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_postreports_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='report_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
