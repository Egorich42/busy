#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^(?P<id>\d+)/(?P<first_name>[\w\-]+)/$', views.show_user_profile, name='show_user_profile'),
]
