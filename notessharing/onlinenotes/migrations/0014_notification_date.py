# Generated by Django 3.1.7 on 2021-08-01 22:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinenotes', '0013_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
