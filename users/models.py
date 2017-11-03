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
from datetime import *



tn ="contragents_documents.doc_type != '0'"
pp = "contragents_documents.doc_type = '0'"


tn2 = "contragents_documents_two.doc_type = '0'"
pp2="contragents_documents.doc_type != '0'"


select_all_documents="SELECT * FROM contragents_documents;"
select_contragents_identificator = "SELECT id FROM contragents;"
select_id_docs = "SELECT parent FROM contragents_documents;"

select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;" 
select_docs_to_mudaky =  "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs_from_mudaky = "SELECT * FROM contragents_documents_two LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id WHERE {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents_two.doc_date;"


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
        resultat = 'сумма задолженности контрагента составляет'+' '+str(round(tn_suma-pp_suma,2))
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'+' '+str(round(pp_suma-tn_suma,2))
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

today = date.today()
this_year = date.today().year
this_month = date.today().month

first_kvartal_end = date(this_year, 3,31)
second_kvartal_end= date(this_year,6,30)
third_kvartal_end= date(this_year,9,30)
four_kvartal_end = date(this_year,12,31)


first_kvartal_start = date(this_year, 1,1)
second_kvartal_start= date(this_year,4,1)
third_kvartal_start= date(this_year,7,1)
four_kvartal_start = date(this_year,10,1)

def current_kvartal():
    if today<first_kvartal_end:
        cur_kvart = first_kvartal_start
    if today > first_kvartal_end and today < second_kvartal_end:
        cur_kvart = second_kvartal_start
    if today >third_kvartal_start and today <third_kvartal_end:
        cur_kvart = third_kvartal_start
    if today > four_kvartal_start and today < four_kvartal_end:
        cur_kvart = four_kvartal_start    
        pass

    return cur_kvart


start_square = str(current_kvartal())
start_month = str(date(this_year, this_month, 1))

def curent_finace_states(start, cursor):
    select_tn_to_pidory = select_docs_to_mudaky.format(tn,  "'"+start+"'",  "'"+str(today)+"'")
    select_tn_from_pidory = select_docs_from_mudaky.format(tn2,  "'"+start+"'",  "'"+str(today)+"'")

    sql_commands_list = (select_tn_to_pidory,select_tn_from_pidory)

    all_docs_tables = [create_list_of_table_values(cursor.execute(f),cursor.description) for f in sql_commands_list]

    summa_poluchenyh_materyalov = [i['summ'] for i in all_docs_tables[1]]
    summa_prodannyh_tovarov = [i['summ'] for i in all_docs_tables[0]]

    usn = str(round(sum(summa_prodannyh_tovarov)*0.05,2))

    nds_polucheny = sum(summa_poluchenyh_materyalov)/6
    nds_otpravleny = sum(summa_prodannyh_tovarov)/6

    full_nds = str (round(nds_otpravleny - nds_polucheny,2))

    return(full_nds, usn)


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



    



