# Generated by Django 3.0.4 on 2020-03-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0003_auto_20200320_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='year',
            field=models.IntegerField(default=2020, verbose_name="Championat's years"),
        ),
    ]
