#! /usr/bin/env python
# -*- coding: utf-8 -*

#python manage.py migrate --run-syncdb
#https://habrahabr.ru/post/313764/
from django.db import migrations
from django.db import models
from django.contrib.auth.models import User
import sqlite3 
from django.db import migrations
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

tn = "contragents_documents.doc_type != '0'"
pp ="contragents_documents.doc_type = '0'"
act = "contragents_documents.doc_type = "
select_all_documents="SELECT * FROM contragents_documents;"

select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs_for_data = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_contragents_identificator = "SELECT id FROM contragents;"


def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 

def perebor(data_sorted, one, two, three):
    albert = []
    for key, group in itertools.groupby(data_sorted, key=lambda x:x[one]):
        a = list(sorted(group, key=lambda item: item[two]))
        suma = sum([f[key] for key in[three] for f in a])
        albert += [sum([f[key] for key in[three] for f in a])]    
    return albert
    pass   

def get_pays_balance(pp_list, tn_list, element_name):
    pp_suma = sum(float(res[element_name]) for res in pp_list)
    tn_suma = sum(float(res[element_name]) for res in tn_list)

    if pp_suma < tn_suma:
        resultat = 'сумма задолженности контрагента составляет'+' '+str(tn_suma-pp_suma)
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'+' '+str(pp_suma-tn_suma)
    if pp_suma == tn_suma:
        resultat = 'OK!'
    return resultat
    pass    



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

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
    ('17','17'),
)

class Client(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    organization_type = models.CharField(max_length=50, db_index=True, verbose_name='Вид организации')
    nalog_system = models.CharField(max_length=200, db_index=True, verbose_name='Система налогооблажения')
    unp = models.PositiveIntegerField(verbose_name='УНП', default=1)
    bank_schet = models.CharField(max_length=100, db_index=True,verbose_name='Банковский счет')
    bank_BIK = models.CharField(max_length=100, db_index=True, verbose_name='IBAN')
    email =  models.EmailField(verbose_name='Е-mail', blank = True) 
    skype= models.CharField(max_length=200, db_index=True, blank = True, verbose_name='Скайп')
    phone =  models.PositiveIntegerField(verbose_name='Телефон', blank = True ,default=1)

class Contragent_identy(models.Model):
    contragent_id =models.CharField(max_length=200, db_index=True, blank = True, verbose_name='Контрагент')
    start_date = models.CharField(max_length=200, db_index=True, blank = True, verbose_name='Даты с')
    end_date = models.CharField(max_length=200, db_index=True, blank = True, verbose_name='по') 
    title = models.CharField(max_length=3, choices=TITLE_CHOICES,db_index=True, blank = True)



    



