#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools
from datetime import *


conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

tn =  "contragents_documents.doc_type != '0'"
pp =  "contragents_documents.doc_type = '0'"


tn_providers = "contragents_documents_two.doc_type = '0'"
pp_providers = "contragents_documents_two.doc_type != '0'"

start_data = "2015-01-01"
ending_data = "2017-09-01"

select_contragents_identificator = "SELECT id FROM contragents;"
select_id_docs = "SELECT parent FROM contragents_documents;"

select_docs_buyers = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs_providers = "SELECT * FROM contragents_documents_two LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id WHERE {} AND contragents_documents_two.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents_two.doc_date;"

select_docs_to = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs_from = "SELECT * FROM contragents_documents_two LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id WHERE {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents_two.doc_date;"


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
        resultat = 'сумма задолженности контрагента составляет'
        res_sum = str(round(tn_suma-pp_suma,2))
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'
        res_sum =str(round(pp_suma-tn_suma,2))
    if pp_suma == tn_suma:
        resultat = 'OK!'
        res_sum = "OKI"
    return (resultat,res_sum)
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
    pass


start_square = str(current_kvartal())
start_month = str(date(this_year, this_month, 1))

def curent_finace_states(start, end, cursor):
    select_tn_to_pidory = select_docs_to_buyers.format(tn,  "'"+start+"'",  "'"+str(end)+"'")
    select_tn_from_pidory = select_docs_from_providers.format(tn_providers,  "'"+start+"'",  "'"+str(end)+"'")

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


def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(select_contragents_identificator),cursor.description)

    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    contargents_id_list = [i['id'] for i in contragents_id]

    for altair in contargents_id_list:
        select_documents_providers = [select_docs_providers.format(doc_two, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc_two in (tn_providers,pp_providers)]
        select_documents_buyers = [select_docs_buyers.format(doc, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (tn,pp)]


        all_buyers_documents = [create_list_of_table_values(cursor.execute(table_two),cursor.description) for table_two in select_documents_buyers]
        all_providers_documents = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents_providers]


        summa_sverki_providers = get_pays_balance(all_buyers_documents[1], all_buyers_documents[0], 'summ')
        summa_sverki_buyers = get_pays_balance(all_providers_documents[1], all_providers_documents[0], 'summ')


        if summa_sverki_providers[0] =='сумма задолженности контрагента составляет' and len(all_buyers_documents[0])>0:
            debts_providers += [{'name':all_buyers_documents[0][0]['name'], 'summa':summa_sverki_buyers[1], 'message':summa_sverki_providers[0]}]
            pass
        
        if summa_sverki_providers[0] =='сумма вашей задолженности составляет' and len(all_buyers_documents[0])>0:
            prepayment_providers += [{'name':all_buyers_documents[0][0]['name'], 'summa':summa_sverki_buyers[1], 'message':summa_sverki_providers[0]}]
            pass

        if summa_sverki_buyers[0] =='сумма задолженности контрагента составляет' and len(all_providers_documents[0])>0:
            debts_buyers += [{'name':all_providers_documents[0][0]['name'], 'summa':summa_sverki_buyers[1], 'message':summa_sverki_providers[0]}]
            pass

        if summa_sverki_buyers[0]  =='сумма вашей задолженности составляет' and len(all_providers_documents[0])>0:
            prepayment_buyers += [{'name':all_providers_documents[0][0]['name'], 'summa':summa_sverki_buyers[1], 'message':summa_sverki_providers[0]}]
            pass

    return(debts_providers,prepayment_providers,debts_buyers,prepayment_buyers)
    pass

