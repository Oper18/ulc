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
    league = serializers.SerializerMethodField()

    def get_league(self, obj):
        return [LeagueSerializer(l).data for l in obj.league.all()]

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
    league = serializers.SerializerMethodField()

    def get_championat(self, obj):
        return ChampionatSerializer(obj.league.championat).data

    def get_league(self, obj):
        return LeagueSerializer(obj.league).data

    class Meta:
        model = Group
        fields = ['id', 'name', 'league', 'championat']


class TeamSerializer(serializers.ModelSerializer):
    league = serializers.SerializerMethodField()
    championat = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    def get_league(self, obj):
        return [LeagueSerializer(g.league).data for g in obj.group.all()]

    def get_championat(self, obj):
        return [ChampionatSerializer(g.league.championat).data for g in obj.group.all()]

    def get_group(self, obj):
        return [GroupSerializer(group).data for group in obj.group.all()]

    class Meta:
        model = Team
        fields = ['id', 'name', 'group', 'league', 'championat', 'logo']


class GameSerializer(serializers.ModelSerializer):
    home = TeamSerializer()
    visitors = TeamSerializer()
    game_date = TimeSlotSerializer()
    championat = ChampionatSerializer()
    group = GroupSerializer()
    # requester = serializers.SerializerMethodField()
    # answer = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'home', 'visitors', 'home_goals', 'visitors_goals', 'game_date', 'championat', 'off',
                  'group', 'tour', 'accepted_date', 'changed_at', 'requester', 'answer']


class TeamBidSerializer(serializers.ModelSerializer):
    championat = ChampionatSerializer()
    team = TeamSerializer()
    # players = serializers.SerializerMethodField()

    class Meta:
        model = TeamBid
        fields = ['id', 'championat', 'players', 'team', 'sended', 'send_date', 'accepted', 'declined', 'accepted_date']


class SuspensionTeamGroupSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    group = GroupSerializer()

    class Meta:
        model = SuspensionTeamGroup
        fields = ['id', 'team', 'group', 'suspension']


class PlayerCurrentTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    championat = ChampionatSerializer()

    class Meta:
        model = PlayerCurrentTeam
        fields = ['id', 'player', 'team', 'championat', 'current', 'number', 'position']


class PlayerSerializer(serializers.ModelSerializer):
    teams = serializers.SerializerMethodField()
    player_teams = PlayerCurrentTeamSerializer(many=True)
    username = serializers.SerializerMethodField()

    def get_teams(self, obj):
        return [TeamSerializer(t).data for t in obj.team.all()]

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Player
        fields = ['id', 'username', 'first_name', 'last_name', 'patronymic', 'teams', 'player_teams', 'is_captain', 'logo',
                  'birthday', 'card_number', 'vk', 'inst']


class PlayerBidSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    source_team = TeamSerializer()
    target_team = TeamSerializer()

    class Meta:
        model = PlayerBid
        fields = ['id', 'player', 'source_team', 'target_team', 'sended_date', 'accepted', 'declined']
