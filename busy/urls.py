#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^', include('info.urls')),
    url(r'^users/', include('users.urls')),
#    url(r'^updater/', include('updater.urls')),              
    url(r'^admin/', admin.site.urls),

]