# Generated by Django 3.0.4 on 2020-04-25 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes_number',
            field=models.IntegerField(default=0),
        ),
    ]
