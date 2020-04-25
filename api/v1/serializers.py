# coding: utf-8

from rest_framework import serializers

from championat.models import Season, Championat, DefaultTimeSlot, TimeSlot, League, Group, Team,\
    Game, TeamBid, SuspensionTeamGroup
from accounts.models import Player, RegistrationKeys, PlayerBid, PlayerCurrentTeam


class SeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = ['id', 'year', 'created_at']


class ChampionatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Championat
        fields = ['id', 'championat', 'season', 'active', 'ended', 'league']


class DefaultTimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = DefaultTimeSlot
        fields = ['id', 'time', 'day', 'championat', 'onetime_games']


class TimeSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlot
        fields = ['id', 'slot', 'championat', 'onetime_games']


class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = ['id', 'name', 'championat', 'logo']


class GroupSerializer(serializers.ModelSerializer):
    championat = serializers.SerializerMethodField()

    def get_championat(self, obj):
        return ChampionatSerializer(obj.league.championat).data

    class Meta:
        model = Group
        fields = ['id', 'name', 'league', 'championat']


class TeamSerializer(serializers.ModelSerializer):
    league = serializers.SerializerMethodField()
    championat = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    def get_league(self, obj):
        leagues = []
        for group in obj.group.all():
            leagues.append(LeagueSerializer(group.league).data)
        return leagues

    def get_championat(self, obj):
        championats = []
        for group in obj.group.all():
            championats.append(ChampionatSerializer(group.league.championat).data)
        return championats

    def get_group(self, obj):
        return [GroupSerializer(group).data for group in obj.group.all()]

    class Meta:
        model = Team
        fields = ['id', 'name', 'group', 'league', 'championat', 'logo']


# class GameSerializer(serializers.ModelSerializer):
#     home = serializers.SerializerMethodField()
#     visitors = serializers.SerializerMethodField()
#     game_date = serializers.SerializerMethodField()
#     championat = serializers.SerializerMethodField()
#     group = serializers.SerializerMethodField()
#     # requester = serializers.SerializerMethodField()
#     # answer = serializers.SerializerMethodField()
#
#     def get_home(self, obj):
#         return TeamSerializer(obj.home).data
#
#     def get_visitors(self, obj):
#         return TeamSerializer(obj.visitors).data
#
#     class Meta:
#         model = Game
#         fields = ['id', 'home', 'visitors', 'home_goals', 'visitors_goals', 'game_date', 'championat', 'off',
#                   'group', 'tour', 'accepted_date', 'changed_at', 'requester', 'answer']
