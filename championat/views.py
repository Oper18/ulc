# coding: utf-8

import os
import datetime
import pytz
import re
import logging

from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse
from django.utils.timezone import now

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from championat.models import Season, League, Group, Team, Game, Championat, TimeSlot, TeamBid, News
from accounts.models import PlayerCurrentTeam, Player

from api.v1.serializers import NewsSerializer


logger = logging.getLogger(__name__)


class ULCBaseTemplateView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(csrf(request))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ULCBaseTemplateView, self).get_context_data(**kwargs)

        context['title'] = settings.SITE_TITLE

        context['navs'] = settings.NAVIGATION

        drop_item = []
        for g in Group.objects.filter(league__in=League.objects.filter(championat__in=
                                                                       Championat.objects.filter(season=
                                                                                                 Season.objects.get(year=datetime.datetime.now().year)))):
            # drop_item.append((g.league.name + g.name, '/league/' + re.sub(r' ', '_', g.league.name.lower()) +
            #                   '/' + re.sub(r' ', '_', g.name) + '/' + str(g.league.championat.id)))
            drop_item.append((g.league.name + g.name, '/league/' + str(g.league.id) +
                              '/' + str(g.id) + '/' + str(g.league.championat.id)))

        addition_navs = [(i[0], i[1]) for i in settings.ADDITION_DROP_NAVIGATION[context['navs'][0][0].encode('utf-8')]]
        context['navs'][0][1] = tuple(drop_item + addition_navs)

        drop_item = []
        for s in Season.objects.all():
            drop_item.append((str(s.year), '/year/' + str(s.year)))
        context['navs'][1][1] = tuple(drop_item)

        return context


class ChampionatView(ULCBaseTemplateView):

    def get_context_data(self, **kwargs):
        context = super(ChampionatView, self).get_context_data(**kwargs)
        if 'league' in self.request.path:
            context['table'] = self.create_table()

        return context

    def create_table(self):
        league = self.request.path.split('/')[2]
        group = self.request.path.split('/')[3]
        teams = []
        for team in Team.objects.filter(group=Group.objects.get(pk=group, league=League.objects.get(pk=league))):
            team_pos = {
                'team': team,
                'games': 0,
                'wins': 0,
                'drawn': 0,
                'loses': 0,
                'rifl': 0,
                'concede': 0,
                'dif': 0,
                'points': 0,
            }
            for game in Game.objects.filter(home=team, off=True, group__isnull=False):
                team_pos['games'] += 1
                team_pos['rifl'] += game.home_goals
                team_pos['concede'] += game.visitors_goals
                if game.home_goals > game.visitors_goals:
                    team_pos['wins'] += 1
                elif game.home_goals < game.visitors_goals:
                    team_pos['loses'] += 1
                else:
                    team_pos['drawn'] += 1
            for game in Game.objects.filter(visitors=team, off=True, group__isnull=False):
                team_pos['games'] += 1
                team_pos['rifl'] += game.visitors_goals
                team_pos['concede'] += game.home_goals
                if game.visitors_goals > game.home_goals:
                    team_pos['wins'] += 1
                elif game.visitors_goals < game.home_goals:
                    team_pos['loses'] += 1
                else:
                    team_pos['drawn'] += 1

            team_pos['dif'] = team_pos['rifl'] - team_pos['concede']
            team_pos['points'] = team_pos['wins'] * 3 + team_pos['drawn']

            teams.append(team_pos)

        return sorted(teams, key=lambda team: team['points'])[::-1]


class CalendarView(ChampionatView):

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        context['calendar'] = []
        for champ in Championat.objects.filter(active=True):
            context['calendar'].append((champ, self.calendar(champ)))

        context['teams'] = Team.objects.all()
        return context


    def calendar(self, championat):
        c = []
        ts = TimeSlot.objects.filter(slot__gte=datetime.datetime.now(pytz.timezone('Europe/Moscow'))). \
            exclude(slot__gt=datetime.datetime.now(pytz.timezone('Europe/Moscow')) + datetime.timedelta(days=6))
        for league in League.objects.filter(championat=championat):
            for group in Group.objects.filter(league=league):
                onetime_games = 1
                for game in Game.objects.filter(group=group):
                    if game.game_date in ts and game.game_date.onetime_games <= onetime_games:
                        ts.exclude(game.game_date)
                    elif game.game_date in ts and game.game_date.onetime_games > onetime_games:
                        onetime_games += 1
                if (datetime.datetime.now() + datetime.timedelta(days=6)).weekday() == 6 and datetime.datetime.now() + datetime.timedelta(days=6) in ts:
                    ts.exclude(slot=datetime.datetime.now(pytz.timezone('Europe/Moscow')) + datetime.timedelta(days=6))
                c.append((league, group, Game.objects.filter(group=group).order_by('game_date'), ts))

        return c


class HistoryULCView(ULCBaseTemplateView):

    def get_context_data(self, **kwargs):
        context = super(HistoryULCView, self).get_context_data(**kwargs)

        for i in self.request.get_full_path().split('/')[::-1]:
            if len(i) > 0:
                year = i
                break
        context['all_history'] = False
        try:
            context['championats'] = Championat.objects.filter(season=Season.objects.get(year=int(year)))
        except:
            context['championats'] = []

        if 'history' in self.request.get_full_path():
            context['seasons'] = []
            for season in Season.objects.all():
                context['seasons'].append((season, Championat.objects.filter(season=season)))
            context['all_history'] = True

        return context


@csrf_protect
def accept_changes(request):
    if request.user.is_staff:
        if Team.objects.get(pk=request.POST.get('home')) != Team.objects.get(pk=request.POST.get('visitors')):
            try:
                game = Game.objects.get(pk=request.POST.get('num'))
                game.home = Team.objects.get(pk=request.POST.get('home'))
                game.visitors = Team.objects.get(pk=request.POST.get('visitors'))
                game.home_goals = request.POST.get('home_goals')
                game.visitors_goals = request.POST.get('visitors_goals')
                if len(Game.objects.filter(game_date=TimeSlot.objects.get(pk=request.POST.get('slot')))) < TimeSlot.objects.get(pk=request.POST.get('slot')).onetime_games:
                    game.game_date = TimeSlot.objects.get(pk=request.POST.get('slot'))
                game.accepted_date = True
                game.changed_at = now()
                game.save()
            except Exception as e:
                logger.error('Saving game changes down: {}'.format(e))
                return JsonResponse({'success': False}, status=400)
            else:
                return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False}, status=400)
    elif request.user.player.all().exists() and request.user.player.all().first().is_captain:
        try:
            game = Game.objects.get(pk=request.POST.get('num'))
            if not game.requester:
                if not game.off and now() >= game.game_date.slot + datetime.timedelta(hours=1, minutes=30):
                    game.home_goals = request.POST.get('home_goals')
                    game.visitors_goals = request.POST.get('visitors_goals')
                    game.requester = request.user
                    game.changed_at = now()
                else:
                    if len(Game.objects.filter(game_date=TimeSlot.objects.get(pk=request.POST.get('slot')))) < TimeSlot.objects.get(pk=request.POST.get('slot')).onetime_games:
                        game.game_date = TimeSlot.objects.get(pk=request.POST.get('slot'))
                        game.changed_at = now()
                        game.requester = request.user
                    else:
                        return JsonResponse({'success': False}, status=400)
                game.save()
            else:
                if not game.off and now() >= game.game_date.slot + datetime.timedelta(hours=1, minutes=30):
                    game.off = True
                    game.answer = request.user
                else:
                    game.accepted_date = True
                    game.answer = request.user
                game.save()
        except Exception as e:
            logger.error('Saving game changes down: {}'.format(e))
            return JsonResponse({'success': False}, status=400)
        else:
            return JsonResponse({'success': True}, status=200)


@csrf_protect
def decline_changes(request):
    if request.user.is_staff:
        if Team.objects.get(pk=request.POST.get('home')) != Team.objects.get(pk=request.POST.get('visitors')):
            try:
                game = Game.objects.get(pk=request.POST.get('num'))
                game.accepted_date = True
                game.changed_at = now()
                game.save()
            except Exception as e:
                logger.error('Decline changes down: {}'.format(e))
                return JsonResponse({'success': False}, status=400)
            else:
                return JsonResponse({'success': True}, status=200)
    elif request.user.player.all().exists() and request.user.player.all().first().is_captain:
        try:
            game = Game.objects.get(pk=request.POST.get('num'))
            if game.requester:
                if not game.off and now() >= game.game_date.slot + datetime.timedelta(hours=1, minutes=30):
                    game.home_goals = None
                    game.visitors_goals = None
                    game.requester = None
                    game.changed_at = now()
                else:
                    game.game_date = None
                    game.changed_at = now()
                    game.requester = None
                game.save()
        except Exception as e:
            logger.error('Decline changes down: {}'.format(e))
            return JsonResponse({'success': False}, status=400)
        else:
            return JsonResponse({'success': True}, status=200)


@csrf_protect
def save_bid(request):
    if request.user.player.is_captain:
        bid_id = request.POST.get('bid')
        championat_id = request.POST.get('championat')
        players = []
        for i in request.POST.keys():
            if 'players' in i:
                players.append(request.POST.getlist(i))
        team_id = request.POST.get('team')
        activity = request.POST.get('activity')

        for player in players:
            pl_team = PlayerCurrentTeam.objects.get(player=Player.objects.get(pk=player[0]),
                                                    team=Team.objects.get(pk=team_id),
                                                    championat=Championat.objects.get(pk=championat_id))
            pl_team.position = player[1] if player[1] and player[1] != '' else pl_team.position
            pl_team.number = int(player[2]) if player[2] and player[2] != '' else pl_team.number
            pl_team.save()

        if bid_id and bid_id != '':
            bid = TeamBid.objects.get(pk=bid_id)
            bid.championat = Championat.objects.get(pk=championat_id)
            for pl in players:
                if Player.objects.get(pk=pl[0]) in bid.players.all():
                    bid.players.remove(Player.objects.get(pk=pl[0]))
                else:
                    bid.players.add(Player.objects.get(pk=pl[0]))
            bid.team = Team.objects.get(pk=team_id)
            bid.save()
        else:
            bid = TeamBid.objects.create(championat = Championat.objects.get(pk=championat_id),
                                         team = Team.objects.get(pk=team_id))
            for pl in players:
                bid.players.add(Player.objects.get(pk=pl[0]))
            bid.save()

        if activity == 'send':
            bid.sended = True
            bid.send_date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
            bid.save()

        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'success': False}, status=400)


@csrf_protect
def answer_bid(request):
    if request.user.is_staff:
        bid = request.POST.get('bid')
        answer = request.POST.get('answer')

        tb = TeamBid.objects.get(pk=bid)

        if answer == 'accept':
            tb.accepted = True
            tb.accepted_date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
            tb.save()

        elif answer == 'decline':
            tb.declined = True
            tb.accepted_date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
            tb.save()

        return JsonResponse({'success': True}, status=200)


@csrf_exempt
def get_news(request):
    news = News.objects.all().order_by('-id')
    qs = NewsSerializer(news, many=True).data
    result = {'news': qs}
    result['correct'] = request.user.is_staff
    return JsonResponse(result)


@csrf_protect
def correct_news(request):
    if request.user.is_staff:
        if 'id' in request.POST.keys():
            new = News.objects.get(pk=request.POST.get('id'))
            head = request.POST.get('head', None)
            head_img = request.FILES.get('head_img', None)
            preread = request.POST.get('preread', None)
            news_body = request.POST.get('news_body', None)
            if head:
                new.head = head
            if head_img:
                new.head_img = head_img
            if preread:
                new.preread = preread
            if news_body:
                new.news_body = news_body
            new.save()
            return JsonResponse({'success': True, 'new_id': new.id}, status=200)
        else:
            print('CREATE NEW')
            new = News.objects.create(head=request.POST.get('head'),
                                      head_img=request.FILES.get('head_img', None),
                                      preread=request.POST.get('preread', None),
                                      news_body=request.POST.get('news_body', None))
            return JsonResponse({'success': True, 'new_id': new.id}, status=200)
        return JsonResponse({'success': False}, status=403)
    return JsonResponse({'success': False, 'reason': 'no permissions'}, status=409)

