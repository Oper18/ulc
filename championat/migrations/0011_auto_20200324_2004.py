# Generated by Django 3.0.4 on 2020-03-24 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0010_auto_20200323_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='home',
        ),
        migrations.AddField(
            model_name='game',
            name='home',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='home', to='championat.Team', verbose_name='Home'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='game',
            name='visitors',
        ),
        migrations.AddField(
            model_name='game',
            name='visitors',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='visitors', to='championat.Team', verbose_name='Visitors'),
            preserve_default=False,
        ),
    ]
