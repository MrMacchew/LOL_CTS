# Generated by Django 2.1.1 on 2018-10-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pushups', '0003_player_accountid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='accountId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pushups.Player'),
        ),
    ]
