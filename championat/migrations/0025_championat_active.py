# Generated by Django 3.0.4 on 2020-04-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0024_auto_20200405_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='championat',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Running championat'),
        ),
    ]
