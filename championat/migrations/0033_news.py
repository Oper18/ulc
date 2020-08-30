# Generated by Django 3.0.4 on 2020-08-25 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championat', '0032_auto_20200508_2309'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head', models.CharField(max_length=256, verbose_name='News head')),
                ('head_img', models.ImageField(blank=True, null=True, upload_to='news_head_image', verbose_name='News image')),
                ('news_body', models.TextField(blank=True, null=True, verbose_name='News body html')),
            ],
        ),
    ]
