# Generated by Django 2.1.1 on 2018-09-25 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushups', '0002_auto_20180924_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='accountId',
            field=models.IntegerField(default=0),
        ),
    ]
