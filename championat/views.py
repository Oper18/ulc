# coding: utf-8

import os
import datetime
import re

from django.shortcuts import render
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse

from championat.models import Season, League, Group, Team, Game, Championat, TimeSlot


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
            drop_item.append((g.league.name + g.name, '/league/' + re.sub(r' ', '_', g.league.name.lower()) +
                              '/' + re.sub(r' ', '_', g.name) + '/' + str(g.league.championat.id)))

        addition_navs = [(i[0], i[1].format(Championat.objects.filter(season=Season.objects.get(year=datetime.datetime.now().year)).last().id))
                         for i in settings.ADDITION_DROP_NAVIGATION[context['navs'][0][0].encode('utf-8')]]
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
        for team in Team.objects.filter(group=Group.objects.get(name=group, league=League.objects.get(name=league))):
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
            for game in Game.objects.filter(home=team, off=True):
                team_pos['games'] += 1
                team_pos['rifl'] += game.home_goals
                team_pos['concede'] += game.visitors_goals
                if game.home_goals > game.visitors_goals:
                    team_pos['wins'] += 1
                elif game.home_goals < game.visitors_goals:
                    team_pos['loses'] += 1
                else:
                    team_pos['drawn'] += 1
            for game in Game.objects.filter(visitors=team, off=True):
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

        for i in self.request.get_full_path().split('/')[::-1]:
            if len(i) > 0:
                ch = i
                break

        try:
            context['calendar'] = self.calendar(Championat.objects.get(pk=ch))
        except:
            context['calendar'] = self.calendar(Championat.objects.all().last())

        context['teams'] = Team.objects.all()

        return context


    def calendar(self, championat):
        c = []
        ts = TimeSlot.objects.filter(slot__gte=datetime.datetime.now()).exclude(slot__gt=datetime.datetime.now() + datetime.timedelta(days=6))
        for league in League.objects.filter(championat=championat):
            for group in Group.objects.filter(league=league):
                for game in Game.objects.filter(group=group):
                    if game.game_date in ts:
                        ts.exclude(game.game_date)
                if (datetime.datetime.now() + datetime.timedelta(days=6)).weekday() == 6 and datetime.datetime.now() + datetime.timedelta(days=6) in ts:
                    ts.exclude(slot=datetime.datetime.now() + datetime.timedelta(days=6))
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
