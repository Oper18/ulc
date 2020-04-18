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
from accounts.models import Player, RegistrationKeys, PlayerCurrentTeam, PlayerBid
from championat.models import Team, DefaultTimeSlot, TimeSlot, Championat, Season, TeamBid

class AccountBaseView(ULCBaseTemplateView):
    def get_context_data(self, **kwargs):
        context = super(AccountBaseView, self).get_context_data(**kwargs)
        context['player_teams'] = []
        context['current_player_teams'] = []
        try:
            player = self.request.user.player
        except:
            player = None
        if not self.request.user.is_anonymous and player:
            for team in self.request.user.player.team.all():
                context['player_teams'].append((team, Player.objects.filter(team=team)))

            for team in PlayerCurrentTeam.objects.filter(player=self.request.user.player, current=True):
                context['current_player_teams'].append((team, Team.objects.filter(group__in=team.team.group.all()),
                                                        PlayerBid.objects.filter(source_team__in=player.team.all(), accepted=False, declined=False).exists()))

            if not player.is_captain:
                context['notifications'] = PlayerBid.objects.filter(source_team__in=player.team.all())
            elif player.is_captain:
                context['notifications'] = PlayerBid.objects.filter(target_team__in=player.team.all())

        if self.request.user.is_staff:
            context['championats'] = Championat.objects.filter(season__in=Season.objects.filter(year__gte=datetime.datetime.now().year))
            context['notifications'] = TeamBid.objects.filter(sended=True, accepted=False)

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
    card = request.POST.get('card')
    vk = request.POST.get('vk')
    inst = request.POST.get('inst')
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
    user.player.card = card
    user.player.vk = vk
    user.player.inst = inst

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


@csrf_protect
def test_email(request):
    user = User.objects.filter(email=request.POST.get('email'))
    if user.exists():
        return JsonResponse({'success': True}, status=400)
    return JsonResponse({'success': True}, status=200)


@csrf_protect
def change_player_team(request):
    if not request.user.is_anonymous and not request.user.player.is_captain:
        source_team = request.POST.get('source_team')
        target_team = request.POST.get('target_team')
        player = request.user.player

        PlayerBid.objects.create(player=player,
                                 source_team=Team.objects.get(pk=source_team),
                                 target_team=Team.objects.get(pk=target_team))

        return JsonResponse({'success': True}, status=200)

    if not request.user.is_anonymous and request.user.player.is_captain:
        bid = PlayerBid.objects.get(pk=request.POST.get('bid'))
        answer = request.POST.get('answer')

        if answer == 'accept':
            bid.accepted = True
            bid.save()
            try:
                bid.player.team.add(bid.target_team)
                bid.player.save()
            except:
                pass
            pct_f = PlayerCurrentTeam.objects.filter(player=bid.player, team=bid.source_team, current=True).last()
            pct_f.current = False
            pct_f.save()
            pct = PlayerCurrentTeam.objects.filter(player=bid.player, team=bid.target_team).order_by('id').last()
            pct.current = True
            pct.championat = pct_f.championat
            pct.save()

        elif answer == 'decline':
            bid.declined = True
            bid.save()

        return JsonResponse({'success': True}, status=200)
