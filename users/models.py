#! /usr/bin/env python
# -*- coding: utf-8 -*

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


def sum_result(income_list):
    return round(sum([i['nds'] for i in income_list if i['full_sum'] != None]),2)


def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 
 

def transform_sql_to_list(cursor, request_command, *condition):
    if len(condition) ==2:
        sql_request = request_command.format(condition[0],condition[1])
    if len(condition) ==3:
        sql_request = request_command.format(condition[0],condition[1],condition[2])
    if len(condition) ==4:
        sql_request = request_command.format(condition[0],condition[1],condition[2],condition[3])
    
    table = create_list_of_table_values(cursor.execute(sql_request),cursor.description)
    return table
    pass


start_square = str(var.current_kvartal())
start_month = str(date(var.this_year, var.this_month, 1))




def curent_finace_states(start, end, cursor,nalog_system):
    from_providers = transform_sql_to_list(cursor, sq_c.select_docs_from_providers, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
    to_buyers = transform_sql_to_list(cursor, sq_c.select_docs_to_buyers, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_ishod_nds_usl = transform_sql_to_list(cursor, sq_c.sel_usl_with_ishod_nds, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )
    list_ishod_nds_tn = transform_sql_to_list(cursor, sq_c.sel_tn_with_ishod_nds, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_vhod_nds_usl = transform_sql_to_list(cursor, sq_c.sel_vhod_usl_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
    list_vhod_nds_tn = transform_sql_to_list(cursor, sq_c.sel_vhod_tn_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_tovary_nds  = transform_sql_to_list(cursor, sq_c.sel_tovary_with_vhod_nds,   "'"+start+"'",  "'"+str(end)+"'" )


    full_vhod_nds = sum_result(list_vhod_nds_usl)+sum_result(list_vhod_nds_tn)+sum_result(list_tovary_nds)
    full_ishod_nds = sum_result(list_ishod_nds_usl)+sum_result(list_ishod_nds_tn)

    if nalog_system == 'NDS':
        now_fin_states = str(round(full_ishod_nds - full_vhod_nds,2))
        tax_system = "NDS" 
    else:
        now_fin_states = str(round(sum([i['summ'] for i in to_buyers])*0.05,2))
        tax_system = "USN" 

    return(now_fin_states, tax_system, full_vhod_nds,full_ishod_nds)
    pass



def transform_sql(select_command,docs,pays,cursor,contragent,data_start,data_end):
    select_documents = [select_command.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (docs,pays)]
    documents_list = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents]

    summa_tn = sum([i['summ']for i in documents_list[0]])
    summa_pp = sum([i['summ']for i in documents_list[1]])
    
    return (documents_list,summa_tn,summa_pp)
    pass
    


def get_sverka(cursor,contragent,data_start,data_end):
    buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cursor,contragent,data_start,data_end)
    buyers_docs_vozvr = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers_vozvr,cursor,contragent,data_start,data_end)
    buyers_docs_dpd = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers_dpd,cursor,contragent,data_start,data_end)


    providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cursor,contragent,data_start,data_end)
    providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cursor,contragent,data_start,data_end)
    providers_docs_vozvr = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers_vozvr,cursor,contragent,data_start,data_end)


    providers_docs_moneyback = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_moneyback, sq_c.pp_providers,cursor,contragent,data_start,data_end)

    contragent_name = cursor.execute(sq_c.select_contragent_name.format("'"+str(contragent)+"'")).fetchall()[0]

    prov_list = providers_docs[0][0]+buyers_docs[0][1]+providers_docs_vozvr[0][1]# delete from this buyers_docs_vozvr[0][1]  

    buyers_list = buyers_docs[0][0]+providers_docs[0][1]+buyers_docs_vozvr[0][1]#buyers_docs_vozvr[0][1] и providers_docs_nodel[0][1]раньше был здесь

    
    suma_tn_prov = providers_docs[1]+providers_docs_nodel[1]+buyers_docs_dpd[2]+providers_docs_vozvr[2]-providers_docs_moneyback[1]
    suma_pp_prov = providers_docs[2]+buyers_docs_vozvr[2]# хз ,что с это сранью делать buyers_docs_vozvr[1]

    suma_tn_buy = buyers_docs[1]
    suma_pp_buy = buyers_docs[2]
    
    inner_summ = round(suma_tn_prov+suma_pp_buy,2)
    outer_summ = round(suma_tn_buy+suma_pp_prov,2)


    result = inner_summ-outer_summ
    return (contragent_name,outer_summ,inner_summ,round(result,2),prov_list,buyers_list) 
    pass



def transform_sql_2(select_command,type_doc,cursor,contragent,data_start,data_end):
    documents_list = transform_sql_to_list(cursor, select_command, type_doc,"'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'")
    doc_sum= sum([i['summ']for i in documents_list])
    return (documents_list,doc_sum)
    pass

     

def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(sq_c.select_contragents_identificator),cursor.description)
    contargents_id_list = [i['id'] for i in contragents_id]
    
    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]
    id_list =[]


    buyers_doc_types = (sq_c.tn_buyers, sq_c.pp_buyers, sq_c.pp_buyers_vozvr, sq_c.pp_buyers_dpd)
    providers_doc_types = (sq_c.tn_providers, sq_c.tn_providers_no_del, sq_c.tn_providers_moneyback,sq_c.pp_providers, sq_c.pp_providers_vozvr)

    def perebor_documentov(doc_tuple,sql_command,contragent):
        documents = []
        for i in doc_tuple:
            proba = transform_sql_2(sql_command,i,cursor,contragent,data_start,data_end)
            documents += [{'documents_list':proba[0],'documents_sum':proba[1]}]
        return documents 

    
    for altair in contargents_id_list:

        buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cursor,altair,data_start,data_end)
        buyers_docs_vozvr = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers_vozvr,cursor,altair,data_start,data_end)
        buyers_docs_dpd = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers_dpd,cursor,altair,data_start,data_end)

        providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cursor,altair,data_start,data_end)
        providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cursor,altair,data_start,data_end)
        providers_docs_vozvr = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers_vozvr,cursor,altair,data_start,data_end)

        providers_docs_moneyback = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_moneyback, sq_c.pp_providers,cursor,altair,data_start,data_end)

        suma_tn_prov = providers_docs[1]+providers_docs_nodel[1]+buyers_docs_dpd[2]+providers_docs_vozvr[2]-providers_docs_moneyback[1]
        suma_pp_prov = providers_docs[2]# добавляю нужныц и работающий в сверке +buyers_docs_vozvr[2] - по нулям
                                        #У возвратной неравильные команды, именно в списке функций
    

        suma_tn_buy = buyers_docs[1]
        suma_pp_buy = buyers_docs[2] 

        inner_summ = suma_tn_prov+suma_pp_buy
        outer_summ = suma_tn_buy+suma_pp_prov 

        if suma_tn_prov>suma_pp_prov and providers_docs[0][0] !=[]:
            if inner_summ-outer_summ>0.1:
                summ = str(round(inner_summ-outer_summ,2))
                for_summator = round(inner_summ-outer_summ,2)
                debts_providers += [{
                                    'name':providers_docs[0][0][0]['name'], 
                                    'contragent_id':providers_docs[0][0][0]['id'], 
                                    'summa':summ, 
                                    'for_sumator':for_summator}]
             
        if suma_tn_prov<suma_pp_prov and providers_docs[0][0] !=[]:
            if outer_summ-inner_summ>0.1:
                summ = str(round(outer_summ-inner_summ,2))
                for_summator = round(outer_summ-inner_summ,2)
                prepayment_providers += [{'name':providers_docs[0][0][0]['name'],
                                        'summa':summ,
                                        'for_sumator':for_summator}]

        if suma_tn_buy<suma_pp_buy and buyers_docs[0][0] !=[]:
            if inner_summ-outer_summ>0.1:
                summ = str(round(inner_summ-outer_summ,2))
                for_summator = round(outer_summ-inner_summ,2)
                debts_buyers += [{'name':buyers_docs[0][0][0]['name'],
                                    'summa':summ,
                                    'for_sumator':for_summator}]            

        if suma_tn_buy>suma_pp_buy and buyers_docs[0][0] !=[]:
            if outer_summ-inner_summ > 0.1:
                summ = str(round(outer_summ-inner_summ,2))
                for_summator = round(outer_summ-inner_summ,2)
                prepayment_buyers += [{'name':buyers_docs[0][0][0]['name'],
                                        'summa':summ,
                                        'for_sumator':for_summator}]            
    

    def summator():
        summa = []
        for x in (debts_providers,prepayment_providers,debts_buyers,prepayment_buyers):
            summa += [round(sum([i['for_sumator'] for i in x]),2)]
        return summa
            
    debts_providers_result = summator()[0]
    prepayment_providers_result = summator()[1]
    debts_buyers_result = summator()[2]
    prepayment_buyers_result = summator()[3]

    return(
            debts_providers,
            prepayment_providers,
            debts_buyers,
            prepayment_buyers, 
            debts_providers_result,
            prepayment_providers_result,
            debts_buyers_result,
            prepayment_buyers_result
            )
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

    

class Client(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    nalog_system = models.CharField(max_length=3, choices=var.taxes,db_index=True, blank = True,verbose_name='Система налогооблажения')
    unp = models.PositiveIntegerField(verbose_name='УНП', default=1)
    bank_schet = models.CharField(max_length=100, db_index=True,verbose_name='Банковский счет')
    bank_BIK = models.CharField(max_length=100, db_index=True, verbose_name='IBAN')
    email = models.EmailField(verbose_name='Е-mail', blank = True) 

