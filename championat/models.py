# coding: utf-8

import datetime

from django.db import models
from django.core.exceptions import FieldError
from django.contrib.auth.models import User
from django.utils.timezone import now


class Season(models.Model):
    year = models.IntegerField(verbose_name='Championat\'s years', default=datetime.datetime.now().year, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)


class Championat(models.Model):
    championat = models.CharField(verbose_name='Championat\'s name', max_length=256)
    season = models.ForeignKey(Season, related_name='championats', on_delete=models.CASCADE, verbose_name='Championat\'s season', null=True)
    active = models.BooleanField(verbose_name='Running championat', default=False)
    ended = models.BooleanField(verbose_name='Championat finished', default=False)

    def __str__(self):
        return self.championat


class DefaultTimeSlot(models.Model):
    DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    )

    time = models.TimeField(verbose_name='Default game slot')
    day = models.IntegerField(verbose_name='Day of week', default=6, choices=DAYS)
    championat = models.ForeignKey(Championat, verbose_name='Championat whis use slot', on_delete=models.CASCADE, related_name='default_slots', null=True)
    onetime_games = models.IntegerField(verbose_name='Number of onetime games', default=2)

    def __str__(self):
        return str(self.day) + ' - ' + str(self.time)


class TimeSlot(models.Model):
    slot = models.DateTimeField(verbose_name='Game time slot', unique=True)
    championat = models.ForeignKey(Championat, related_name='slots', on_delete=models.CASCADE, verbose_name='Championat\'s slot', null=True)
    onetime_games = models.IntegerField(verbose_name='Number of onetime games', default=2)

    def __str__(self):
        return str(self.slot)


class League(models.Model):
    name = models.CharField(verbose_name='League name', max_length=128)
    championat = models.ForeignKey(Championat, on_delete=models.CASCADE, null=True, related_name='league')
    logo = models.ImageField(upload_to='league_logo', null=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(verbose_name='Group name', max_length=128)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return '{}: {}-{}'.format(self.league.championat.championat, self.league.name, self.name)

    @property
    def teams(self):
        return Team.objects.all()


class Team(models.Model):
    name = models.CharField(verbose_name='Team name', max_length=255)
    group = models.ManyToManyField(Group, related_name='group')
    logo = models.ImageField(upload_to='team_logo', null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    home = models.ForeignKey(Team, verbose_name='Home', related_name='home', on_delete=models.CASCADE)
    visitors = models.ForeignKey(Team, verbose_name='Visitors', related_name='visitors', on_delete=models.CASCADE)
    home_goals = models.IntegerField(default=0, null=True)
    visitors_goals = models.IntegerField(default=0, null=True)
    game_date = models.ForeignKey(TimeSlot, related_name='games', verbose_name='Game time', null=True, on_delete=models.SET_NULL)
    championat = models.ForeignKey(Championat, on_delete=models.CASCADE, null=True)
    off = models.BooleanField(verbose_name='Is game ended', default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    tour = models.CharField(verbose_name='Group tour', max_length=64, null=True)
    accepted_date = models.BooleanField(verbose_name='Is game time accept', default=False)
    changed_at = models.DateTimeField(verbose_name='Date of last changes', auto_now_add=True)
    requester = models.ForeignKey(User, verbose_name='Send request', related_name='requester', on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(User, verbose_name='Answer request', related_name='answer', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.home.name + '-' + self.visitors.name

    @property
    def check_date(self):
        return now() < self.game_date.slot

    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        if self.home == self.visitors:
            raise FieldError
        else:
            super(Game, self).save_base(raw, force_insert, force_update, using, update_fields)


class TeamBid(models.Model):
    championat = models.ForeignKey(Championat, verbose_name='Team bid for championat', on_delete=models.SET_NULL, null=True, related_name='team_bids')
    players = models.ManyToManyField('accounts.Player', verbose_name='Players in bid')
    team = models.ForeignKey(Team, verbose_name='Team\' bid', on_delete=models.SET_NULL, null=True, related_name='team_bids')
    sended = models.BooleanField(verbose_name='Is bid sended', default=False)
    send_date = models.DateTimeField(verbose_name='Send bid date', auto_now_add=True)
    accepted = models.BooleanField(verbose_name='Is bid accepted by admin', default=False)
    accepted_date = models.DateTimeField(verbose_name='Accept bid date', null=True)

    def __str__(self):
        champ = self.championat.championat if self.championat else self.pk
        team = self.team.name if self.team else ''
        return '{}, {}'.format(champ, team)
