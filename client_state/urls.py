#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views
from client_state.views import clients_list

urlpatterns = [
	url(r'^$', clients_list.as_view(template_name="singles/clients/clients_list.html")),
    url(r'^(?P<name>[-\w]+)/$', views.client_detail, name='client_detail'), 
       
]


