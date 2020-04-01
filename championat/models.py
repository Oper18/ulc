# coding: utf-8

import datetime

from django.db import models


class Season(models.Model):
    year = models.IntegerField(verbose_name='Championat\'s years', default=datetime.datetime.now().year, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)


class Championat(models.Model):
    championat = models.CharField(verbose_name='Championat\'s name', max_length=256)
    season = models.ForeignKey(Season, related_name='championats', on_delete=models.CASCADE, verbose_name='Championat\'s season', null=True)

    def __str__(self):
        return self.championat


class TimeSlot(models.Model):
    slot = models.DateTimeField(verbose_name='Game time slot', unique=True)
    championat = models.ForeignKey(Championat, related_name='slots', on_delete=models.CASCADE, verbose_name='Championat\'s slot', null=True)

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
        return self.name


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
    game_date = models.ForeignKey(TimeSlot, related_name='games', verbose_name='Game time', null=True, on_delete=models.CASCADE)
    championat = models.ForeignKey(Championat, on_delete=models.CASCADE, null=True)
    off = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    tour = models.CharField(verbose_name='Group tour', max_length=64, null=True)

    def __str__(self):
        return self.home.name + '-' + self.visitors.name
