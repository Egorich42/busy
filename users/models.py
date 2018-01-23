#! /usr/bin/env python
# -*- coding: utf-8 -*

#python manage.py migrate --run-syncdb
#https://habrahabr.ru/post/313764/
from . import sql_commands as sq_c
from . import variables as var
from datetime import *

from django.db import migrations
from django.db import models
from django.contrib.auth.models import User
from django.db import migrations
from itertools import groupby
from collections import defaultdict
from operator import itemgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

import win32com.client
import os
import xlwt

def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
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



def get_paginator(cursor, table_name, request_name, vals_on_page,request):
    paginator = Paginator(create_list_of_table_values(cursor.execute(sq_c.docs_on_main.format(table_name,request_name)),cursor.description),vals_on_page)
    all_documents = get_pages(request,paginator)
    return all_documents




start_square = str(var.current_kvartal())
start_month = str(date(var.this_year, var.this_month, 1))

def curent_finace_states(start, end, cursor,nalog_system):
    select_tn_to_pidory = sq_c.select_docs_to_buyers.format(sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'")
    select_tn_from_pidory = sq_c.select_docs_from_providers.format(sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'")

    sql_commands_list = (select_tn_to_pidory,select_tn_from_pidory)

    all_docs_tables = [create_list_of_table_values(cursor.execute(f),cursor.description) for f in sql_commands_list]

    summa_poluchenyh_materyalov = [i['summ'] for i in all_docs_tables[1]]
    summa_prodannyh_tovarov = [i['summ'] for i in all_docs_tables[0]]

    usn = str(round(sum(summa_prodannyh_tovarov)*0.05,2))
    nds_polucheny = sum(summa_poluchenyh_materyalov)/6
    nds_otpravleny = sum(summa_prodannyh_tovarov)/6
    full_nds = str (round(nds_otpravleny - nds_polucheny,2))

    if nalog_system == 'НДС':
        now_fin_states = full_nds
        tax_system = "НДС" 
    else:
        now_fin_states = usn
        tax_system = "УСН" 

    return(now_fin_states, tax_system)



def transform_sql(select_command,docs,pays,cursor,contragent,data_start,data_end):
    select_documents = [select_command.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (docs,pays)]
    documents_list = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents]
    summa_tn = sum([i['summ']for i in documents_list[0]])
    summa_pp = sum([i['summ']for i in documents_list[1]])
#    print(len(documents_list[0]))
    
    return (documents_list,summa_tn,summa_pp)
    pass
    



def get_sverka(cursor,contragent,data_start,data_end):
    buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cursor,contragent,data_start,data_end)
    buyers_docs_vozvr = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers_vozvr,cursor,contragent,data_start,data_end)

    providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cursor,contragent,data_start,data_end)
    providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cursor,contragent,data_start,data_end)
    providers_docs_vozvr = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers_vozvr,cursor,contragent,data_start,data_end)

    contragent_name = cursor.execute(sq_c.select_contragent_name.format("'"+str(contragent)+"'")).fetchall()[0]

    prov_list = providers_docs_nodel[0][0]+providers_docs[0][0]+buyers_docs[0][0]+buyers_docs_vozvr[0][0]+providers_docs_vozvr[0][1]
    buyers_list = buyers_docs[0][1]+providers_docs[0][1]+providers_docs_nodel[0][0]
    
    suma_tn_prov = providers_docs[1]+providers_docs_nodel[1]+providers_docs_vozvr[2]
    suma_pp_prov = providers_docs[2]+buyers_docs_vozvr[1]

    suma_tn_buy = buyers_docs[1]
    suma_pp_buy = buyers_docs[2]
    
    
    inner_summ = round(suma_tn_prov+suma_pp_buy,2)
    outer_summ = round(suma_tn_buy+suma_pp_prov,2)  

    result = inner_summ-outer_summ

    #PROVIDER DOC NODEL - с ними работал

    return (contragent_name,outer_summ,inner_summ,round(result,2),prov_list,buyers_list) 
    pass


def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(sq_c.select_contragents_identificator),cursor.description)
    contargents_id_list = [i['id'] for i in contragents_id]
    
    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]
    id_list =[]

    
    for altair in contargents_id_list:

        buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cursor,altair,data_start,data_end)
        buyers_docs_vozvr = transform_sql(sq_c.select_documents_to_buyers,sq_c.pp_buyers_vozvr, sq_c.pp_buyers,cursor,altair,data_start,data_end)

        providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cursor,altair,data_start,data_end)
        providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cursor,altair,data_start,data_end)
        providers_docs_vozvr = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers_vozvr,cursor,altair,data_start,data_end)

        suma_tn_prov = providers_docs[1]+providers_docs_nodel[1]+providers_docs_vozvr[2]
        suma_pp_prov = providers_docs[2]+buyers_docs_vozvr[1]
        

        suma_tn_buy = buyers_docs[1]
        suma_pp_buy = buyers_docs[2] 

        inner_summ = suma_tn_prov+suma_pp_buy
        outer_summ = suma_tn_buy+suma_pp_prov 

        if suma_tn_prov>suma_pp_prov and providers_docs[0][0] !=[]:
            message = 'сумма вашей задолженности составляет'
            summ = str(round(inner_summ-outer_summ,2))
            if summ != '0':
                debts_providers += [{'name':providers_docs[0][0][0]['name'], 'contragent_id':providers_docs[0][0][0]['id'], 'message':message, 'summa':summ}]
             
        if suma_tn_prov<suma_pp_prov and providers_docs[0][0] !=[]:
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(outer_summ-inner_summ,2))
            if summ != '0':
                prepayment_providers += [{'name':providers_docs[0][0][0]['name'],'contragent_id':providers_docs[0][0][0]['id'],  'message':message, 'summa':summ}]

        if suma_tn_buy<suma_pp_buy and buyers_docs[0][0] !=[]:
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(inner_summ-outer_summ,2))
            if summ != '0':
                debts_buyers += [{'name':buyers_docs[0][0][0]['name'],'contragent_id':buyers_docs[0][0][0]['id'],  'message':message, 'summa':summ}]            

        if suma_tn_buy>suma_pp_buy and buyers_docs[0][0] !=[]:
            message = 'сумма вашей задолженности составляет'
            summ = str(round(outer_summ-inner_summ,2))
            if summ != '0':
                prepayment_buyers += [{'name':buyers_docs[0][0][0]['name'],'contragent_id':buyers_docs[0][0][0]['id'], 'message':message, 'summa':summ}]            
    
    return(debts_providers,prepayment_providers,debts_buyers,prepayment_buyers)
    pass




class Client(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    nalog_system = models.CharField(max_length=3, choices=var.taxes,db_index=True, blank = True,verbose_name='Система налогооблажения')
    unp = models.PositiveIntegerField(verbose_name='УНП', default=1)
    bank_schet = models.CharField(max_length=100, db_index=True,verbose_name='Банковский счет')
    bank_BIK = models.CharField(max_length=100, db_index=True, verbose_name='IBAN')
    email = models.EmailField(verbose_name='Е-mail', blank = True) 

