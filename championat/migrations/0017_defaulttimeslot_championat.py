# Generated by Django 3.0.4 on 2020-04-01 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0016_auto_20200401_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaulttimeslot',
            name='championat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_slots', to='championat.Championat', verbose_name='Championat whis use slot'),
        ),
    ]
