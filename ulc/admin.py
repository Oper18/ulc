# coding: utf-8

from django.contrib import admin
from django import forms

from championat.models import Season, League, Group, Team, Game, Championat, TimeSlot, DefaultTimeSlot
from accounts.models import Player, RegistrationKeys


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'year')

admin.site.register(Season, SeasonAdmin)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'championat')
    list_filter = ('championat',)

admin.site.register(League, LeagueAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league')
    list_filter = ('league',)

admin.site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('group',)

admin.site.register(Team, TeamAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'home', 'visitors', 'changed_at', 'group')
    list_filter = ('group', 'home', 'visitors')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(GameAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['game_date'].required = False
        form.base_fields['tour'].required = False
        form.base_fields['group'].required = False
        form.base_fields['requester'].required = False
        form.base_fields['answer'].required = False
        form.base_fields['home_goals'].required = False
        form.base_fields['visitors_goals'].required = False

        return form

admin.site.register(Game, GameAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'number')
    list_filter = ('position', 'team')

    def name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(PlayerAdmin, self).get_form(request, obj, change, **kwargs)
        form.base_fields['logo'].required = False

        return form

admin.site.register(Player, PlayerAdmin)


class RegistrationKeysAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegistrationKeys, RegistrationKeysAdmin)


class ChampionatAdmin(admin.ModelAdmin):
    list_display = ('id', 'championat')
    list_filter = ('season',)

admin.site.register(Championat, ChampionatAdmin)


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot', 'championat')
    list_filter = ('championat',)

admin.site.register(TimeSlot, TimeSlotAdmin)


class DefaultTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'day', 'championat')
    list_filter = ('day', 'championat')

admin.site.register(DefaultTimeSlot, DefaultTimeSlotAdmin)
