# Generated by Django 3.0.5 on 2020-04-30 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateTimeField(default=datetime.datetime.today),
        ),
    ]