# coding: utf-8

from django.urls import path, re_path
from django.urls import include, path
from rest_framework import routers

from rest_framework_swagger.views import get_swagger_view

from .views import *


# router = routers.DefaultRouter()
# router.register(r'api/test', TestView)

ulc_view = get_swagger_view(title='ULC API')

urlpatterns = [
    re_path(r'^api/docs/$', ulc_view),
    # path('', include(router.urls)),
    # re_path(r'^api/login/$', LoginView.as_view(), name='api_login'),
    re_path(r'^api/login/$', api_login, name='api_login'),

    re_path(r'^api/test/$', TestView.as_view({
        'get': 'list',
        'post': 'create',
    })),

    re_path(r'^api/test/(?P<pk>\d+)/$', TestView.as_view({
        'get': 'list',
        'put': 'update',
        'delete': 'destroy',
    })),

    re_path(r'api/test2/$', TestAPIView.as_view()),
    re_path(r'api/league/[0-9]+/[0-9]+/[0-9]+/$', ChampionatAPIView.as_view()),
]