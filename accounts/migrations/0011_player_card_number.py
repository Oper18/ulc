# Generated by Django 3.0.4 on 2020-04-18 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200417_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='card_number',
            field=models.CharField(default='-', max_length=128, verbose_name="FCLM's card number (US/KK/ST)"),
        ),
    ]