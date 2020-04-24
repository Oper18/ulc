# coding: utf-8

from django.urls import path, re_path
from django.urls import include, path
from rest_framework import routers

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .views import *


router = routers.DefaultRouter()
router.register(r'api/test', TestView)

urlpatterns = [
    path('', include(router.urls)),
    # re_path(r'^api/login/$', LoginView.as_view(), name='api_login'),
    re_path(r'^api/login/$', api_login, name='api_login'),
]