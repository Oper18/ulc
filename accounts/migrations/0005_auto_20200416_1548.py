# Generated by Django 3.0.4 on 2020-04-16 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0024_auto_20200405_0849'),
        ('accounts', '0004_player_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ManyToManyField(null=True, to='championat.Team', verbose_name="Player's team"),
        ),
    ]
