#! /usr/bin/env python
# -*- coding: utf-8 -*

import datetime
from datetime import date

from . import sql_commands as sq_c
from django.db import migrations
from django.db import models
from django.contrib.auth.models import User
from django.db import migrations

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django import forms

from forge import create_list_of_table_values, taxes


def get_pages(request,paginator):
    page = request.GET.get('page')
    try:
        all_pages = paginator.page(page)
    except PageNotAnInteger:
        all_pages = paginator.page(1)
    except EmptyPage:
        all_pages = paginator.page(paginator.num_pages)
    return all_pages    
    pass



def get_paginator(cursor, table_name, request_name, vals_on_page,request):
    paginator = Paginator(create_list_of_table_values(cursor.execute(sq_c.docs_on_main.format(table_name,request_name)),cursor.description),vals_on_page)
    all_documents = get_pages(request,paginator)
    return all_documents

    

class Client(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    rus_name = models.CharField(max_length=200, db_index=True, verbose_name='Название на русском')
    nalog_system = models.CharField(max_length=3, choices=taxes,db_index=True, blank = True,verbose_name='Система налогооблажения')

