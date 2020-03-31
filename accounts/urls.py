# coding: utf-8

from django.urls import re_path

from accounts.views import AccountBaseView, ulc_login, RegistrationView, invite_player, check_registration_key, \
    register_user, ulc_logout


urlpatterns = [
    re_path(r'^account/$', AccountBaseView.as_view(template_name="accounts/accounts.html"), name='user_account'),
    re_path(r'^account/(?P<id>[0-9]+)/$', AccountBaseView.as_view(template_name="accounts/accounts.html"), name='user_account'),
    re_path(r'^registration/$', check_registration_key(RegistrationView.as_view(template_name="accounts/registration.html")), name='registration'),
    re_path(r'^ajax/login/$', ulc_login, name='ajax_login'),
    re_path(r'^ajax/logout/$', ulc_logout, name='ajax_logout'),
    re_path(r'^ajax/invite/$', invite_player, name='ajax_invite'),
    re_path(r'^ajax/registration/$', register_user, name='ajax_register'),
]