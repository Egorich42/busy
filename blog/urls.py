#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.create_post, name='create_post'),
]
