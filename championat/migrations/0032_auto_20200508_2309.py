# Generated by Django 3.0.4 on 2020-05-08 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0031_auto_20200424_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='home_goals',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='visitors_goals',
            field=models.IntegerField(null=True),
        ),
    ]
