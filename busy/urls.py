#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^', include('info.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^updater/', include('updater.urls')),
    url(r'^office/', include('client_state.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
