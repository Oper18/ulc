# Generated by Django 3.0.4 on 2020-04-24 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0030_suspensionteamgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='group',
            field=models.ManyToManyField(related_name='teams', to='championat.Group'),
        ),
    ]
