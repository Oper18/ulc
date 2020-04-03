# Generated by Django 3.0.4 on 2020-04-03 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('championat', '0022_auto_20200402_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to=settings.AUTH_USER_MODEL, verbose_name='Answer request'),
        ),
        migrations.AlterField(
            model_name='game',
            name='requester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL, verbose_name='Send request'),
        ),
    ]
