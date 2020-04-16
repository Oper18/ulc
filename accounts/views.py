# coding: utf-8

import re
import random
import string
import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from championat.views import ULCBaseTemplateView
from accounts.models import Player, RegistrationKeys
from championat.models import Team, DefaultTimeSlot, TimeSlot, Championat, Season

class AccountBaseView(ULCBaseTemplateView):
    def get_context_data(self, **kwargs):
        context = super(AccountBaseView, self).get_context_data(**kwargs)
        context['player_teams'] = []
        try:
            player = self.request.user.player
        except:
            player = None
        if not self.request.user.is_anonymous and player:
            for team in self.request.user.player.team.all():
                context['player_teams'].append((team, Player.objects.filter(team=team)))

        if self.request.user.is_staff:
            context['championats'] = Championat.objects.filter(season__in=Season.objects.filter(year__gte=datetime.datetime.now().year))

        return context


class RegistrationView(ULCBaseTemplateView):
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        try:
            context['team'] = RegistrationKeys.objects.get(key=self.request.GET.get('key')).inviter.player.team.all().first()
        except:
            context['team'] = None
        return context


@csrf_exempt
def invite_player(request):
    try:
        player = request.user.player
    except:
        player = None
    if player and player.is_captain or request.user.is_staff:
        alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
        key = ''.join(random.choice(alphabet) for _ in range(32))
        try:
            RegistrationKeys.objects.create(key=key,
                                            inviter=request.user,
                                            valid_date=now()+datetime.timedelta(days=1))
        except Exception as e:
            print(e)
        return JsonResponse({'success': True, 'key': key}, status=200)
    else:
        return JsonResponse({'success': False}, status=400)


@csrf_protect
def ulc_login(request):
    user = request.POST.get('username')
    password = request.POST.get('password')

    ath = authenticate(username=user, password=password)
    if ath:
        login(request, ath)
        redir = re.search(r'\?next=.+', request.POST.get('uri')) if request.POST.get('uri') else None
        try:
            redir = redir.group(0).split('=')[-1]
        except Exception as e:
            redir = '/'
        return JsonResponse({'success': True, 'redirect': redir}, status=200)
    else:
        return JsonResponse({'success': False}, status=400)


@csrf_exempt
def ulc_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'redirect': '/'}, status=200)


@csrf_protect
def register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    patronymic = request.POST.get('patronymic')
    birthday = datetime.datetime.strptime(request.POST.get('birthday'), '%Y-%m-%d').date()
    keyparam = re.search(r'\?key=\w+', request.POST.get('uri')).group(0).split('=')[-1]
    key = RegistrationKeys.objects.get(key=keyparam)
    try:
        team = key.inviter.player.team
    except Exception as e:
        team = None

    try:
        user = User.objects.create_user(username, email, password)
    except Exception as e:
        return JsonResponse({'success': False}, status=400)

    user.first_name = first_name
    user.last_name = last_name

    user.player.first_name = first_name
    user.player.last_name = last_name
    user.player.team.add = team
    user.player.patronymic = patronymic
    user.player.birthday = birthday

    user.save()

    key.inactive = True
    key.save()
    return JsonResponse({'success': True, 'redirect': '/account/{}'.format(user.id)}, status=200)


def check_registration_key(request_view):
    def wrapper(request):
        try:
            key = RegistrationKeys.objects.get(key=request.GET.get('key'))
        except Exception as e:
            return HttpResponseForbidden
        else:
            if not key.inactive:
                return request_view(request)
            else:
                return HttpResponseForbidden
    return wrapper


@csrf_exempt
def default_slots_ajax(request):
    championat = Championat.objects.get(pk=request.POST.get('championat'))
    if request.user.is_staff:
        create_default_slots(championat)


def create_default_slots(championat):
    for dst in DefaultTimeSlot.objects.filter(championat=championat):
        if dst.day > datetime.datetime.now().weekday():
            delta_days = dst.day - datetime.datetime.now().weekday()
        elif dst.day == datetime.datetime.now().weekday():
            delta_days = 7
        elif dst.day < datetime.datetime.now().weekday():
            delta_days = 7 - datetime.datetime.now().weekday() - dst.day

        year = (datetime.datetime.now() + datetime.timedelta(days=delta_days)).year
        month = (datetime.datetime.now() + datetime.timedelta(days=delta_days)).month
        day = (datetime.datetime.now() + datetime.timedelta(days=delta_days)).day

        new_ts, created = TimeSlot.objects.get_or_create(slot=datetime.datetime.combine(datetime.date(year, month, day), dst.time),
                                                         championat=championat,
                                                         onetime_games=dst.onetime_games)


@csrf_protect
def test_username(request):
    user = User.objects.filter(username=request.POST.get('username'))
    if user.exists():
        return JsonResponse({'success': True}, status=400)
    return JsonResponse({'success': True}, status=200)
