# Generated by Django 3.0.4 on 2020-04-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20200418_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='trip',
            field=models.IntegerField(default=0, verbose_name='Number of trips for FCLM'),
        ),
    ]
