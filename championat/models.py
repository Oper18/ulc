# coding: utf-8

import datetime

from django.db import models


class Season(models.Model):
    year = models.IntegerField(verbose_name='Championat\'s years', default=datetime.datetime.now().year, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)


class League(models.Model):
    name = models.CharField(verbose_name='League name', max_length=128)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, related_name='league')
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
    game_date = models.DateTimeField(verbose_name='Game time', null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    off = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    tour = models.CharField(verbose_name='Group tour', max_length=64, null=True)

    def __str__(self):
        return self.home.name + '-' + self.visitors.name
