# Generated by Django 2.1.1 on 2018-10-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushups', '0007_remove_match_pushups'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateField(default='2018-10-01'),
        ),
    ]
