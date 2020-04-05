# Generated by Django 3.0.4 on 2020-04-05 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0023_auto_20200403_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_date',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='championat.TimeSlot', verbose_name='Game time'),
        ),
    ]
