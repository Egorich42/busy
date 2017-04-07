#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_post/$', views.create_post, name='create_post'),
    url(r'^$', views.post_list, name='post_list'),
#    url(r'^$', views.client, name='client'),
]