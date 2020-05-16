# coding: utf-8

import json
import re

from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .serializers import SeasonSerializer, ChampionatSerializer, DefaultTimeSlotSerializer, TimeSlotSerializer, \
    LeagueSerializer, GroupSerializer, TeamSerializer, GameSerializer, TeamBidSerializer, SuspensionTeamGroupSerializer, \
    PlayerCurrentTeamSerializer, PlayerSerializer, PlayerBidSerializer

from championat.models import Season, Championat, DefaultTimeSlot, TimeSlot, League, Group, Team, \
    Game, TeamBid, SuspensionTeamGroup
from accounts.models import Player, RegistrationKeys, PlayerBid, PlayerCurrentTeam

from championat.views import ChampionatView, CalendarView


class TestView(viewsets.ModelViewSet):
    """
    This is test method where will be testing different serializers
    GET - return all info about objects, ?pk=<id> - return info about choosen object
    POST - create new object
    PUT - /<pk> will update choosen object
    DELETE - /<pk> will delete choosen object
    """
    serializer_class = ChampionatSerializer
    queryset = Championat.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = re.search(r'[0-9]+', self.request.path)
        pk = pk.group(0) if pk else None
        qs = super(TestView, self).get_queryset()
        return qs if not pk else qs.filter(pk=pk)

    def create(self, request, *args, **kwargs):
        return super(TestView, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(TestView, self).update(request, *args, **kwargs)


class TestAPIView(APIView):
    """
    Another test API view, like /api/test
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        champ = ChampionatView()
        request_copy = request
        request_copy.path = '/league/10/20/1/'
        champ.request = request_copy
        context = champ.get_context_data()
        for i in context['table']:
            i['team'] = TeamSerializer(i['team']).data
        return Response(context['table'])

    def post(self, request, *args, **kwargs):
        return Response({'success': 'return'})


class ChampionatModelView(viewsets.ModelViewSet):
    """
    List championats, if not use <pk> in path usage of query params <eded=True/False> and <active=True/False> will filter result
    """
    serializer_class = ChampionatSerializer
    queryset = Championat.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ended = self.request.query_params.get('ended')
        active = self.request.query_params.get('active')

        pk = re.search(r'[0-9]+', self.request.path)
        pk = pk.group(0) if pk else None
        qs = super(ChampionatModelView, self).get_queryset()

        if ended and not pk:
            qs = qs.filter(ended=ended)
        if active and not pk:
            qs = qs.filter(active=active)

        return qs if not pk else qs.filter(pk=pk)


class LeagueModelView(viewsets.ModelViewSet):
    """
    List leagues, if not use <pk> in path usage of query params <eded=True/False> and <active=True/False> will filter result
    """
    serializer_class = LeagueSerializer
    queryset = League.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ended = self.request.query_params.get('ended')
        active = self.request.query_params.get('active')

        pk = re.search(r'[0-9]+', self.request.path)
        pk = pk.group(0) if pk else None
        qs = super(LeagueModelView, self).get_queryset()

        if ended and not pk:
            qs = qs.filter(championat__ended=ended)
        if active and not pk:
            qs = qs.filter(championat__active=active)

        return qs if not pk else qs.filter(pk=pk)

    def create(self, request, *args, **kwargs):
        season = None
        if request.data.get('season'):
            season, created = Season.objects.get_or_create(year=request.data.get('season'))
            season = season
        if request.data.get('championat') and isinstance(request.data.get('championat'), str):
            season = Season.objects.all().order_by('created_at').last() if not season else season
            champ, created = Championat.objects.get_or_create(championat=request.data.get('championat'),
                                                              season=season)
            champ_id = champ.id
            request.data['championat'] = champ_id
            if 'season' in request.data: del request.data['season']
        return super(LeagueModelView, self).create(request, *args, **kwargs)


class GroupModelView(viewsets.ModelViewSet):
    """
    List groups, if not use <pk> in path usage of query params <eded=True/False> and <active=True/False> will filter result
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ended = self.request.query_params.get('ended')
        active = self.request.query_params.get('active')

        pk = re.search(r'[0-9]+', self.request.path)
        pk = pk.group(0) if pk else None
        qs = super(GroupModelView, self).get_queryset()

        if ended and not pk:
            qs = qs.filter(league__championat__ended=ended)
        if active and not pk:
            qs = qs.filter(league__championat__active=active)

        return qs if not pk else qs.filter(pk=pk)

    def create(self, request, *args, **kwargs):
        season = None
        championat = None
        if request.data.get('season'):
            season, created = Season.objects.get_or_create(year=request.data.get('season'))
            season = season
        if request.data.get('championat') and isinstance(request.data.get('championat'), str):
            season = Season.objects.all().order_by('created_at').last() if not season else season
            championat, created = Championat.objects.get_or_create(championat=request.data.get('championat'),
                                                                   season=season)
            championat = championat
        if request.data.get('league') and isinstance(request.data.get('league'), str):
            championat = Championat.objects.all().order_by('season__created_at').last() if not championat else championat
            league, created = League.objects.get_or_create(name=request.data.get('league'),
                                                           championat=championat)
            league_id = league.id
            request.data['league'] = league_id
            if 'season' in request.data: del request.data['season']
            if 'championat' in request.data: del request.data['championat']
        return super(GroupModelView, self).create(request, *args, **kwargs)


class ChampionatAPIView(APIView):
    """
    Get tournament table: /league/<league_pk>/<group_pk>/<championat_pk>/
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        champ = ChampionatView()
        request_copy = request
        request_copy.path = re.sub(r'/api', '', request.path)
        champ.request = request_copy
        context = champ.get_context_data()
        for i in context['table']:
            i['team'] = TeamSerializer(i['team']).data
        return Response(context['table'])


class CalendarAPIView(APIView):
    """
    Get calendar
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        calendar = CalendarView()
        request_copy = request
        request_copy.path = re.sub(r'/api', '', request.path)
        calendar.request = request_copy
        context = calendar.get_context_data()

        response = {}

        response['teams'] = [TeamSerializer(i).data for i in context['teams']]

        calendar = []
        for champ in context['calendar']:
            # calendar.append((ChampionatSerializer(champ[0]).data, ()))
            l = []
            for i in champ[1]:
                l.append(((GameSerializer(game).data for game in i[2]),
                          (TimeSlotSerializer(ts).data for ts in i[3])))

            calendar.append((ChampionatSerializer(champ[0]).data, l))

        response['calendar'] = calendar

        return Response(response)

    def post(self, request, format=None):
        if request.user.is_staff:
            game = Game.objects.get(pk=request.data.get('game_id'))
            timeslot = TimeSlot.objects.get(pk=request.data.get('ts_id')) if request.data.get('ts_id') else None
            if timeslot:
                game.game_date = timeslot
                game.save()
            return Response(GameSerializer(game).data)
        if request.user.player.is_captain:
            game = Game.objects.get(pk=request.data.get('game_id'))
            timeslot = TimeSlot.objects.get(pk=request.data.get('ts_id')) if request.data.get('ts_id') else None
            if timeslot and not game.accepted_date:
                game.game_date = timeslot
                game.save()
            return Response(GameSerializer(game).data)
        return Response({'message': 'No permissions'})


class HistoryAPIView(APIView):

    def get(self, request, format=None):
        response = {'champs': []}
        for champ in Championat.objects.all():
            if champ.ended:
                winners = self.get_league_winner(champ)
            else:
                winners = None
            response['champs'].append(ChampionatSerializer(champ).data, winners)

        return Response(response)

    def post(self, request, format=None):
        return Response({'message': 'Method not allowed'})

    def get_league_winner(self, champ):
        res = {}
        for l in champ.league.all():
            res[l.name] = {}
            for g in l.group.all():
                winner = None
                for team in Team.objects.filter(group=g):
                    winner_points = 0
                    for game in Game.objects.filter(group=g, home=team):
                        if game.home_goals > game.visitors_goals:
                            winner_points += 3
                        elif game.home_goals == game.visitors_goals:
                            winner_points += 1
                    for game in Game.objects.filter(group=g, visitors=team):
                        if game.home_goals < game.visitors_goals:
                            winner_points += 3
                        elif game.home_goals == game.visitors_goals:
                            winner_points += 1
                    if not winner:
                        winner = (team, winner_points)
                    else:
                        if winner[1] < winner_points:
                            winner = (team, winner_points)

                res[l.name][g.name] = winner

        return res


@csrf_exempt
def api_login(request):
    token, status = Token.objects.get_or_create(user=User.objects.get(username=json.loads(request.body).get('username')))
    return JsonResponse({'token': token.key}, status=200)
