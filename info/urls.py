#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.MainPageView.as_view()),
    url(r'^contacts/', TemplateView.as_view(template_name="landing/contacts.html")),
]

