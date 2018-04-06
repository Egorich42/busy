#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^dif/$', views.insert_into_excel, name='insert_into_excel'),
]
