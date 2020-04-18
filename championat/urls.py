# coding: utf-8

from django.urls import re_path
from django.contrib.auth.decorators import login_required

from championat.views import ChampionatView, CalendarView, ULCBaseTemplateView, HistoryULCView, accept_changes, \
    decline_changes, save_bid, answer_bid


urlpatterns = [
    re_path(r'^$', ULCBaseTemplateView.as_view(template_name="championat/index.html"), name='championat'),

    # re_path(r'^calendar/(?P<id>[0-9]+)/$',
    #         login_required(CalendarView.as_view(template_name="championat/calendar.html")),
    #         name='calendar'),

    re_path(r'^calendar/$',
            login_required(CalendarView.as_view(template_name="championat/calendar.html")),
            name='calendar'),

    re_path(r'^rules/$', ULCBaseTemplateView.as_view(template_name="championat/rules.html"), name='rules'),

    re_path(r'^league/(?P<league>\w+)/(?P<group>\w+)/(?P<id>[0-9]+)/$',
            login_required(ChampionatView.as_view(template_name="championat/league.html")),
            name='league_schedule'),

    re_path(r'^league/(?P<league>\w+)/(?P<id>[0-9]+)/(?P<team>\w+)/$',
            login_required(CalendarView.as_view(template_name="championat/calendar.html")),
            name='calendar_team'),

    re_path(r'^year/(?P<year>[0-9]{4})/$',
            login_required(HistoryULCView.as_view(template_name='championat/history.html')),
            name='season_history'),

    re_path(r'^year/(?P<year>[0-9]{4})/(?P<id>\w+)/$',
            login_required(HistoryULCView.as_view(template_name='championat/history.html')),
            name='season_history'),

    re_path(r'^year/(?P<year>[0-9]{4})/(?P<id>\w+)/(?P<league>\w+)/$',
            login_required(HistoryULCView.as_view(template_name='championat/history.html')),
            name='season_history'),

    re_path(r'^history/$',
            login_required(HistoryULCView.as_view(template_name='championat/history.html')),
            name='history'),

    re_path(r'^ajax/request/accept/$', accept_changes, name='game_changes_accpet'),
    re_path(r'^ajax/request/decline/$', decline_changes, name='game_changes_decline'),

    re_path(r'^ajax/save_bid/$', save_bid, name='save_bid'),
    re_path(r'^ajax/answer_bid/$', answer_bid, name='answer_bid'),
]