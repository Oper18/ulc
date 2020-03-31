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
from championat.models import Team

class AccountBaseView(ULCBaseTemplateView):
    pass


class RegistrationView(ULCBaseTemplateView):
    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['team'] = RegistrationKeys.objects.get(key=self.request.GET.get('key')).inviter.player.all().first().team.all().first()
        return context


@csrf_exempt
def invite_player(request):
    player = Player.objects.get(user=request.user)
    if player.is_captain:
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
        return JsonResponse({'success':False}, status=400)


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

    try:
        user = User.objects.create_user(username, email, password)
    except Exception as e:
        return JsonResponse({'success': False}, status=400)
    user.first_name = first_name
    user.last_name = last_name
    user.save()
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
