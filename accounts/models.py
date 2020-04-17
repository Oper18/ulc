# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from championat.models import Team, Championat


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ManyToManyField(Team, verbose_name='Player\'s team', through='PlayerCurrentTeam')
    position = models.CharField(verbose_name='Player\' position', max_length=128, null=True)
    is_captain = models.BooleanField(default=False)
    logo = models.ImageField(upload_to='players_logo', null=True)
    number = models.IntegerField(verbose_name='Player number', null=True)
    first_name = models.CharField(verbose_name='First name', max_length=128, null=True)
    last_name = models.CharField(verbose_name='Last name', max_length=128, null=True)
    patronymic = models.CharField(verbose_name='Patronymic', null=True, max_length=128)
    birthday = models.DateField(verbose_name='Birth date', null=True)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()


class PlayerBid(models.Model):
    player = models.ForeignKey(Player, related_name='player_bids', on_delete=models.CASCADE)
    source_team = models.ForeignKey(Team, related_name='source_teams', on_delete=models.SET_NULL, null=True)
    target_team = models.ForeignKey(Team, related_name='target_teams', on_delete=models.SET_NULL, null=True)
    sended_date = models.DateTimeField(verbose_name='Team change bid date', auto_now_add=True)
    accepted = models.BooleanField(verbose_name='Is bid accepted by captain', default=False)
    declined = models.BooleanField(verbose_name='Is bid declined by captain', default=False)

    def __str__(self):
        return str(self.pk)


class PlayerCurrentTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    championat = models.ForeignKey(Championat, on_delete=models.SET_NULL, null=True)
    current = models.BooleanField(verbose_name='Is team current', default=False)

    def __str__(self):
        return '{} - {}'.format(self.player.user.username, self.team.name)
