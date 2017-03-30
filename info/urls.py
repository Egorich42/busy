#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.show_main_page, name='index'),
]