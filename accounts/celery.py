# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os
import datetime

from celery import Celery
from celery.task import periodic_task
from celery.schedules import crontab

from django.utils.timezone import now


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ulc.settings')

app = Celery('accounts')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()


@periodic_task(run_every=crontab(hour='*/1'))
def debug_task():
    from accounts.models import RegistrationKeys
    for key in RegistrationKeys.objects.filter(inactive=False, valid_date__gte=now()):
        key.inactive = False
        key.save()


@periodic_task(run_every=crontab(minute=0, hour=23, day_of_week='sun'))
def create_slots():
    from accounts.views import create_default_slots
    from championat.models import Championat, Season

    for championat in Championat.objects.filter(season__in=Season.objects.filter(year__gte=datetime.datetime.now().year)):
        create_default_slots(championat)
