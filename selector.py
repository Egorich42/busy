#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools
from datetime import *
import win32com.client

import sql_commands as sq_c
import variables as var

conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

start_data = "2014-01-01"
ending_data = "2017-11-11"

data_start = "2014-01-01"
data_end = "2017-11-11"
contragent = 6

def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 



def current_kvartal():
    if var.today<var.first_kvartal_end:
        cur_kvart = var.first_kvartal_start
    if var.today > var.first_kvartal_end and var.today < var.second_kvartal_end:
        cur_kvart = var.second_kvartal_start
    if var.today >var.third_kvartal_start and var.today <var.third_kvartal_end:
        cur_kvart = third_kvartal_start
    if var.today > var.four_kvartal_start and var.today < var.four_kvartal_end:
        cur_kvart = var.four_kvartal_start    
        pass
    return cur_kvart
    pass


start_square = str(current_kvartal())
start_month = str(date(var.this_year, var.this_month, 1))

def curent_finace_states(start, end, cursor):
    select_tn_to_pidory = select_docs_to_buyers.format(sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'")
    select_tn_from_pidory = select_docs_from_providers.format(sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'")

    sql_commands_list = (select_tn_to_pidory,select_tn_from_pidory)

    all_docs_tables = [create_list_of_table_values(cursor.execute(f),cursor.description) for f in sql_commands_list]

    summa_poluchenyh_materyalov = [i['summ'] for i in all_docs_tables[1]]
    summa_prodannyh_tovarov = [i['summ'] for i in all_docs_tables[0]]

    usn = str(round(sum(summa_prodannyh_tovarov)*0.05,2))
    nds_polucheny = sum(summa_poluchenyh_materyalov)/6
    nds_otpravleny = sum(summa_prodannyh_tovarov)/6
    full_nds = str (round(nds_otpravleny - nds_polucheny,2))

    return(full_nds, usn)


def show_fin_states(data_start, data_end, cursor, nalog_system):
    current_fin_states = curent_finace_states(data_start, data_end,cursor)

    if nalog_system == 'НДС':
        now_fin_states = current_fin_states[0]
        tax_system = "НДС" 
    else:
        now_fin_states = current_fin_states[1]
        tax_system = "УСН"           
        pass    
    pass
    return(now_fin_states, tax_system)

def get_pays_balance(pp_list, tn_list, element_name):
    pp_suma = sum(float(res[element_name]) for res in pp_list)
    tn_suma = sum(float(res[element_name]) for res in tn_list)

    if pp_suma < tn_suma:
        resultat = 'сумма задолженности контрагента составляет'
        res_sum = str(round(tn_suma-pp_suma,2))
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'
        res_sum =str(round(pp_suma-tn_suma,2))
    if pp_suma == tn_suma:
        resultat = 'Задолженности нет!'
        res_sum = "Ничего"
    return (resultat,res_sum)
    pass   



def show_sverka(cursor):
    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    select_documents_buyers = [sq_c.select_documents_to_buyers.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (sq_c.tn_buyers,sq_c.pp_buyers)]
    select_documents_providers = [sq_c.select_documents_from_providers.format(doc_two, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc_two in (sq_c.tn_providers,sq_c.pp_providers)]


    all_buyers_documents = [create_list_of_table_values(cursor.execute(table_two),cursor.description) for table_two in select_documents_buyers]
    all_providers_documents = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents_providers]

    summa_sverki_buyers = get_pays_balance(all_buyers_documents[1], all_buyers_documents[0], 'summ')
    summa_sverki_providers = get_pays_balance(all_providers_documents[1], all_providers_documents[0], 'summ')
    print(all_buyers_documents)
    pass

show_sverka(cur)

def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(sq_c.select_contragents_identificator),cursor.description)

    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    contargents_id_list = [i['id'] for i in contragents_id]

    for altair in contargents_id_list:
        select_documents_providers = [sq_c.select_docs_prodanoe.format(doc_two, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc_two in (sq_c.tn_buyers,sq_c.pp_buyers)]
        select_documents_buyers = [sq_c.select_docs_poluchenoe.format(doc, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (sq_c.tn_providers,sq_c.pp_providers)]

        

        all_buyers_documents = [create_list_of_table_values(cursor.execute(table_two),cursor.description) for table_two in select_documents_buyers]
        all_providers_documents = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents_providers]

        summa_sverki_providers = get_pays_balance(all_buyers_documents[1], all_buyers_documents[0], 'summ')
        summa_sverki_buyers = get_pays_balance(all_providers_documents[1], all_providers_documents[0], 'summ')


        if summa_sverki_providers[0] =='сумма задолженности контрагента составляет' and len(all_buyers_documents[0])>0:
            debts_providers += [{'name':all_buyers_documents[0][0]['name'],'message':summa_sverki_providers[0], 'summa':summa_sverki_providers[1]}]
            pass
        
        if summa_sverki_providers[0] =='сумма вашей задолженности составляет' and len(all_buyers_documents[0])>0:
            prepayment_providers += [{'name':all_buyers_documents[0][0]['name'], 'message':summa_sverki_providers[0], 'summa':summa_sverki_providers[1]}]
            pass

        if summa_sverki_buyers[0] != 'Задолженности нет!' and summa_sverki_buyers[0] == 'сумма задолженности контрагента составляет':
            debts_buyers += [{'name':all_providers_documents[0][0]['name'],'message':summa_sverki_buyers[0], 'summa':summa_sverki_buyers[1]}]
            pass

        if summa_sverki_buyers[0]  =='сумма вашей задолженности составляет' and len(all_providers_documents[0])>0:
            prepayment_buyers += [{'name':all_providers_documents[0][0]['name'],'message':summa_sverki_buyers[0], 'summa':summa_sverki_buyers[1]}]
            pass
    return(debts_providers,prepayment_providers,debts_buyers,prepayment_buyers)
    pass









        if suma_tn_prov > suma_pp_prov:
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(suma_tn_prov-suma_pp_prov,2)) 
            prepayment_providers += [{'name':suma_tn_prov[0][0]['name'],'message':message, 'summa':str(summ)}]
     


        if suma_tn_buy<suma_pp_buy :
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(suma_pp_buy-suma_tn_buy,2)) 
            debts_buyers += [{'name':suma_tn_buy[0][0]['name'],'message':message, 'summa':str(summ)}]
 
            pass

        if suma_tn_buy > suma_pp_buy:
            message = 'сумма вашей задолженности составляет'
            summ = str(round(suma_pp_buy-suma_tn_buy,2))
            prepayment_buyers += [{'name':suma_tn_buy[0][0]['name'],'message':message, 'summa':str(summ)}]
            pass

def transform_sql(select_comamnd,docs,pays,cursor,contragent):
    select_documents = [select_comamnd.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (docs,pays)]
    documents_list = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents]
    
    summa_tn = sum([i['summ']for i in documents_list[0]])
    summa_pp = sum([i['summ']for i in documents_list[1]])
    
    return (бdocuments_list,summa_tn,summa_pp)
    pass
    


def show_sverka(cursor):
    summa_buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cur,contragent)
    summa_providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cur,contragent)
    summa_providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cur,contragent)
 
    suma1 = summa_providers_docs[1]
    suma2 = summa_providers_docs[2]
    suma21 = summa_providers_docs_nodel[1]   
    suma3 = summa_buyers_docs[1]
    suma4 = summa_buyers_docs[2]

    testsum = suma1+suma21+suma3
    testsum2 = suma2+suma4
    
    print(suma1,suma2, suma21,suma3,suma4)
    print(testsum- testsum2)
    pass

show_sverka(cur)


def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(sq_c.select_contragents_identificator),cursor.description)
    contargents_id_list = [i['id'] for i in contragents_id]
    
    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    
    for altair in contargents_id_list:

        buyers_docs = transform_sql(sq_c.select_documents_to_buyers,sq_c.tn_buyers, sq_c.pp_buyers,cur,altair)
        providers_docs = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers, sq_c.pp_providers,cur,altair)
        providers_docs_nodel = transform_sql(sq_c.select_documents_from_providers,sq_c.tn_providers_no_del, sq_c.pp_providers,cur,altair)
 
        suma_tn_prov = providers_docs[1]+providers_docs_nodel[1]
        suma_pp_prov = providers_docs[2]
#        suma_tn_prov_del = summa_providers_docs_nodel[1]   
        suma_tn_buy = buyers_docs[1]
        suma_pp_buy = buyers_docs[2]



        if suma_tn_prov<suma_pp_prov :
            message = 'сумма вашей задолженности составляет'
            summ = str(round(suma_tn_prov-suma_pp_prov,2))
            debts_providers += [{'name':suma_tn_prov[0][0]['name'],'message':message, 'summa':summ}]
             
            pass

        if suma_tn_prov > suma_pp_prov:
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(suma_tn_prov-suma_pp_prov,2)) 
            prepayment_providers += [{'name':suma_tn_prov[0][0]['name'],'message':message, 'summa':summ}]
     


        if suma_tn_buy<suma_pp_buy :
            message = 'сумма задолженности контрагента составляет'
            summ = str(round(suma_pp_buy-suma_tn_buy,2)) 
            debts_buyers += [{'name':suma_tn_buy[0][0]['name'],'message':message, 'summa':summ}]
 
            pass

        if suma_tn_buy > suma_pp_buy:
            message = 'сумма вашей задолженности составляет'
            summ = str(round(suma_pp_buy-suma_tn_buy,2))
            prepayment_buyers += [{'name':suma_tn_buy[0][0]['name'],'message':message, 'summa':summ}]
            pass
 
    return(debts_providers,prepayment_providers,debts_buyers,prepayment_buyers)
    pass