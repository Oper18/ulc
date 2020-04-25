# coding: utf-8

import json
import re

from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .serializers import SeasonSerializer, ChampionatSerializer, DefaultTimeSlotSerializer, TimeSlotSerializer, \
    LeagueSerializer, GroupSerializer, TeamSerializer, GameSerializer, TeamBidSerializer, SuspensionTeamGroupSerializer, \
    PlayerCurrentTeamSerializer, PlayerSerializer, PlayerBidSerializer

from championat.models import Season, Championat, DefaultTimeSlot, TimeSlot, League, Group, Team, \
    Game, TeamBid, SuspensionTeamGroup
from accounts.models import Player, RegistrationKeys, PlayerBid, PlayerCurrentTeam


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


@csrf_exempt
def api_login(request):
    token, status = Token.objects.get_or_create(user=User.objects.get(username=json.loads(request.body).get('username')))
    return JsonResponse({'token': token.key}, status=200)
