#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Post


class PostItemInline(admin.TabularInline):
    model = Post
    raw_id_field = ['post']

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','created','slug']


admin.site.register(Post, PostAdmin)
