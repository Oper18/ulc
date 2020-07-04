# Generated by Django 3.0.4 on 2020-07-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200524_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playercurrentteam',
            name='position',
            field=models.CharField(choices=[('ВРТ', 'GK'), ('ЗАШ', 'DEF'), ('ПЗЩ', 'MID'), ('НАП', 'FRW')], max_length=128, null=True, verbose_name="Player' position"),
        ),
    ]
