# coding: utf-8

from django.urls import re_path
from django.contrib.auth.decorators import login_required

from accounts.views import AccountBaseView, ulc_login, RegistrationView, invite_player, check_registration_key, \
    register_user, ulc_logout, test_username, test_email, change_player_team


urlpatterns = [
    re_path(r'^account/$', AccountBaseView.as_view(template_name="accounts/accounts.html"), name='user_account'),
    re_path(r'^account/(?P<id>[0-9]+)/$', login_required(AccountBaseView.as_view(template_name="accounts/accounts.html")), name='user_account'),
    re_path(r'^registration/$', check_registration_key(RegistrationView.as_view(template_name="accounts/registration.html")), name='registration'),
    re_path(r'^ajax/login/$', ulc_login, name='ajax_login'),
    re_path(r'^ajax/logout/$', ulc_logout, name='ajax_logout'),
    re_path(r'^ajax/invite/$', invite_player, name='ajax_invite'),
    re_path(r'^ajax/registration/$', register_user, name='ajax_register'),
    re_path(r'^ajax/testusername/$', test_username, name='ajax_testusername'),
    re_path(r'^ajax/testemail/$', test_email, name='ajax_testemail'),

    re_path(r'^ajax/change_team/$', change_player_team, name='change_team'),

    re_path(r'^team/(?P<id>[0-9]+)/$',
            login_required(AccountBaseView.as_view(template_name="accounts/team_profile.html")),
            name='league_schedule'),
]