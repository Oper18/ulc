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

    for championat in Championat.objects.filter(season__in=Season.objects.filter(year__gte=now().year)):
        create_default_slots(championat)


@periodic_task(run_every=crontab(hour='*/1'))
def test_requests():
    from championat.models import Game, TimeSlot

    for game in Game.objects.filter(changed_at__lte=now() + datetime.timedelta(hours=-72), game_date__slot__gt=now(), off=False, accepted_date=False).\
            exclude(game_date__slot__range=(now(), now() + datetime.timedelta(hours=24))):
        game.requester = None
        game.game_date = None
        game.save()

    for game in Game.objects.filter(changed_at__lte=now() + datetime.timedelta(hours=-72), game_date__slot__lt=now(), off=False):
        if game.home_goals and game.visitors_goals:
            game.off = True
            game.save()

    for game in Game.objects.filter(game_date__slot__range=(now(), now() + datetime.timedelta(hours=24))):
        game.accepted_date = True
        game.save()
