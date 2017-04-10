#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible
from .models import *

admin.site.register(Post)

# Register your models here.
class Post(admin.ModelAdmin):
    list_display = ['id',   'post_name',]
    list_filter = [ 'id']


