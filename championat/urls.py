# coding: utf-8

from django.urls import re_path

from championat.views import ChampionatView, CalendarView, ULCBaseTemplateView, HistoryULCView


urlpatterns = [
    re_path(r'^$', ULCBaseTemplateView.as_view(template_name="championat/index.html"), name='championat'),
    re_path(r'^calendar/(?P<year>[0-9]{4})/$', CalendarView.as_view(template_name="championat/calendar.html"), name='calendar'),
    re_path(r'^rules/$', ULCBaseTemplateView.as_view(template_name="championat/rules.html"), name='rules'),
    re_path(r'^league/(?P<league>\w+)/(?P<group>\w+)/(?P<year>[0-9]{4})/$', ChampionatView.as_view(template_name="championat/league.html"), name='league_schedule'),
    re_path(r'^league/(?P<league>\w+)/(?P<year>[0-9]{4})/(?P<team>\w+)/$', CalendarView.as_view(template_name="championat/calendar.html"), name='calendar_team'),
    re_path(r'^year/(?P<year>[0-9]{4})/$', HistoryULCView.as_view(template_name='championat/history.html'), name='season_history'),
    re_path(r'^year/(?P<year>[0-9]{4})/(?P<league>\w+)/$', HistoryULCView.as_view(template_name='championat/history.html'), name='season_history'),
    re_path(r'^history/$', HistoryULCView.as_view(template_name='championat/history.html'), name='history'),
]