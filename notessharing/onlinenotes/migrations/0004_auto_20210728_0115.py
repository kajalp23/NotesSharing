# Generated by Django 3.1.7 on 2021-07-27 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinenotes', '0003_auto_20210728_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='uploadingnotes',
            field=models.FileField(upload_to='media/files/'),
        ),
    ]
