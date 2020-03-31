# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

from championat.models import Team


class Player(models.Model):
    user = models.ForeignKey(User, related_name='player', on_delete=models.CASCADE)
    team = models.ManyToManyField(Team, verbose_name='Player\'s team')
    position = models.CharField(verbose_name='Player\' position', max_length=128, null=True)
    is_captain = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='players_logo', null=True)
    number = models.IntegerField(verbose_name='Player number', null=True)

    def __str__(self):
        return self.user.username


class RegistrationKeys(models.Model):
    key = models.CharField(verbose_name='unique registration key', unique=True, max_length=256)
    inviter = models.ForeignKey(User, related_name='invite_registration', on_delete=models.CASCADE)
    valid_date = models.DateTimeField(verbose_name='Experiation key time')
    creation_date = models.DateTimeField(verbose_name='Created key date', auto_now_add=True)
    inactive = models.BooleanField(verbose_name='Was key used', default=False)

    def __str__(self):
        return self.inviter.username