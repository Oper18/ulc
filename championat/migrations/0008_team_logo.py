# Generated by Django 3.0.4 on 2020-03-21 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0007_auto_20200321_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.ImageField(null=True, upload_to='team_logo'),
        ),
    ]
