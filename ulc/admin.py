# coding: utf-8

from django.contrib import admin
from championat.models import Season, League, Group, Team, Game, Championat, TimeSlot, DefaultTimeSlot
from accounts.models import Player, RegistrationKeys


class SeasonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Season, SeasonAdmin)


class LeagueAdmin(admin.ModelAdmin):
    pass

admin.site.register(League, LeagueAdmin)


class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)


class TeamAdmin(admin.ModelAdmin):
    pass

admin.site.register(Team, TeamAdmin)


class GameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Game, GameAdmin)


class PlayerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)


class RegistrationKeysAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegistrationKeys, RegistrationKeysAdmin)


class ChampionatAdmin(admin.ModelAdmin):
    pass

admin.site.register(Championat, ChampionatAdmin)


class TimeSlotAdmin(admin.ModelAdmin):
    pass

admin.site.register(TimeSlot, TimeSlotAdmin)


class DefaultTimeSlotAdmin(admin.ModelAdmin):
    pass

admin.site.register(DefaultTimeSlot, DefaultTimeSlotAdmin)
