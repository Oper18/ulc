# coding: utf-8

from __future__ import absolute_import, unicode_literals

import os

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
