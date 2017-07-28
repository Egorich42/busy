#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible
from .models import *

admin.site.register(Client)

# Register your models here.
class Client(admin.ModelAdmin):
    list_display = ['id', 'name',]
    list_filter = [ 'id']


