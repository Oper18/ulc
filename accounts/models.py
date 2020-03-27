# coding: utf-8

from django.contrib.auth.models import User
from django.db import models

from championat.models import Team


class Player(models.Model):
    user = models.ForeignKey(User, related_name='player', on_delete=models.CASCADE)
    team = models.ManyToManyField(Team, verbose_name='Player\'s team')
    position = models.CharField(verbose_name='Player\' position', max_length=128, null=True)
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
