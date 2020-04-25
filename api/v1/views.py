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

from championat.views import ChampionatView


class TestView(viewsets.ModelViewSet):
    """
    This is test method where will be testing different serializers
    GET - return all info about objects, ?pk=<id> - return info about choosen object
    POST - create new object
    PUT - /<pk> will update choosen object
    DELETE - /<pk> will delete choosen object
    """
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
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
        print('## ', context)
        # return Response([ChampionatSerializer(championat).data for championat in Championat.objects.all()])
        return Response(context['table'])

    def post(self, request, *args, **kwargs):
        print('# ', args)
        print('## ', kwargs)
        print('### ', request.data.keys())
        return Response({'success': 'return'})


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



@csrf_exempt
def api_login(request):
    token, status = Token.objects.get_or_create(user=User.objects.get(username=json.loads(request.body).get('username')))
    return JsonResponse({'token': token.key}, status=200)
