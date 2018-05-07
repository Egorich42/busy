#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.get_acess_to_office, name='get_acess_to_office'), 
    url(r'^(?P<name>[-\w]+)/$', views.client_detail, name='client_detail'), 
       
]
