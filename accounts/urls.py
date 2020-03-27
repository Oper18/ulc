# coding: utf-8

from django.urls import re_path

from accounts.views import AccountBaseView


urlpatterns = [
    re_path(r'^account/$', AccountBaseView.as_view(template_name="accounts/accounts.html"), name='user_account'),
]