# coding: utf-8

import json

from django.contrib.auth.models import User
from django.http import JsonResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .serializers import ChampionatSerializer, GroupSerializer, TeamSerializer
from championat.models import Championat, Group, Team


class TestView(viewsets.ModelViewSet):
    # serializer_class = ChampionatSerializer
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.request.query_params.get('pk')
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