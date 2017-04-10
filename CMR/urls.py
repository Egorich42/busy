#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^mail/$', views.post_email, name='post_email'),
    url(r'^$', views.client_list, name='client_list'),
    url(r'^create/$', views.create_client, name='create_client'),
    url(r'^(?P<id>\d+)/$', views.client_profile, name='client_profile'),
]
