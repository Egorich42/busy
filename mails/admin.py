#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible
from .models import Client

admin.site.register(Client)

# Register your models here.
class Client(admin.ModelAdmin):
    list_display = ['id',   'email', 'icon', 'name', 'phone','skype', 'telegram', 
                     'bank_schet','spheres', 'description', 'individual_number']
    list_filter = [ 'id']


