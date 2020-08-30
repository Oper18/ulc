# coding: utf-8

from django.urls import path, re_path
from django.urls import include, path
from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views

from .views import *


# router = routers.DefaultRouter()
# router.register(r'api/test', TestView)

ulc_view = get_swagger_view(title='ULC API')

urlpatterns = [
    re_path(r'^api/docs/$', ulc_view),
    # path('', include(router.urls)),
    re_path('^api/token/$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('^api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    re_path(r'^api/test/$', TestView.as_view({
        'get': 'list',
        'put': 'create',
    })),

    re_path(r'^api/test/(?P<pk>\d+)/$', TestView.as_view({
        'get': 'list',
        'post': 'update',
        'delete': 'destroy',
    })),

    re_path(r'api/test2/$', TestAPIView.as_view()),

    re_path(r'^api/championat/$', ChampionatModelView.as_view({
        'get': 'list',
        'put': 'create',
    })),

    re_path(r'^api/championat/(?P<pk>\d+)/$', ChampionatModelView.as_view({
        'get': 'list',
        'post': 'update',
        'delete': 'destroy',
    })),

    re_path(r'^api/league/$', LeagueModelView.as_view({
        'get': 'list',
        'put': 'create',
    })),

    re_path(r'^api/league/(?P<pk>\d+)/$', LeagueModelView.as_view({
        'get': 'list',
        'post': 'update',
        'delete': 'destroy',
    })),

    re_path(r'^api/group/$', GroupModelView.as_view({
        'get': 'list',
        'put': 'create',
    })),

    re_path(r'^api/group/(?P<pk>\d+)/$', GroupModelView.as_view({
        'get': 'list',
        'post': 'update',
        'delete': 'destroy',
    })),

    re_path(r'api/league/[0-9]+/[0-9]+/[0-9]+/$', ChampionatAPIView.as_view()),
    re_path(r'api/calendar/$', CalendarAPIView.as_view()),
    re_path(r'api/history/$', HistoryAPIView.as_view()),
    re_path(r'api/get_news/$', NewsAPIView.as_view({
        'get': 'list',
        'put': 'create',
    })),
    re_path(r'api/get_news/(?P<pk>\d+)/$', NewsAPIView.as_view({
        'post': 'update',
    })),
]
