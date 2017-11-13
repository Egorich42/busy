#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3
import os
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools
from datetime import *
import win32com.client

import commands

conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()


select_contragents_identificator = commands.select_contragents_identificator
select_id_docs = commands.select_id_docs
select_docs_poluchenoe = commands.select_docs_poluchenoe
select_docs_prodanoe = commands.select_docs_prodanoe

select_docs_to = commands.select_docs_to
select_docs_from = commands.select_docs_from

tn_providers  =commands.tn_providers
pp_providers =commands.pp_providers
tn_buyers =commands.tn_buyers
pp_buyers =commands.pp_buyers



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
    select_tn_to_pidory = select_docs_to_buyers.format(tn_providers,  "'"+start+"'",  "'"+str(end)+"'")
    select_tn_from_pidory = select_docs_from_providers.format(tn_buyers,  "'"+start+"'",  "'"+str(end)+"'")

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

contragent_id = '6'
start_data = "2015-12-29"
ending_data = "2017-11-10"

def act_sverki(contragent_id,start_data,ending_data):
    all_docums_providers = [select_docs_poluchenoe.format(doc, "'"+str(contragent_id)+"'", "'"+start_data+"'", "'"+ending_data+"'") for doc in (pp_providers,tn_providers)]
    all_docums_buyers = [select_docs_prodanoe.format(doc, "'"+str(contragent_id)+"'", "'"+start_data+"'", "'"+ending_data+"'") for doc in (pp_buyers,tn_buyers)]

    buyers_pp_and_tn = [create_list_of_table_values(cur.execute(doc),cur.description) for doc in (all_docums_buyers)]
    providers_pp_and_tn = [create_list_of_table_values(cur.execute(doc),cur.description) for doc in (all_docums_providers)]
    print(len(providers_pp_and_tn[0]))

    pp_suma = sum(float(res['summ']) for res in providers_pp_and_tn[0])+sum(float(res['summ']) for res in buyers_pp_and_tn[0])
    tn_suma = sum(float(res['summ']) for res in providers_pp_and_tn[1])+sum(float(res['summ']) for res in buyers_pp_and_tn[0])



    pass

act_sverki(contragent_id,start_data,ending_data)

"""
def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(select_contragents_identificator),cursor.description)

    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    contargents_id_list = [i['id'] for i in contragents_id]

    for altair in contargents_id_list:
        select_documents_providers = [select_docs_prodanoe.format(doc_two, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc_two in (tn_buyers,pp_buyers)]
        select_documents_buyers = [select_docs_poluchenoe.format(doc, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (tn,pp)]

        
        all_providers_documents = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents_providers]
        all_buyers_documents = [create_list_of_table_values(cursor.execute(table_two),cursor.description) for table_two in select_documents_buyers]

        summa_sverki_providers = get_pays_balance(all_providers_documents[1], all_providers_documents[0], 'summ')
        summa_sverki_buyers = get_pays_balance(all_buyers_documents[1], all_buyers_documents[0], 'summ')


        if summa_sverki_buyers[0] != 'Задолженности нет!' and summa_sverki_buyers[0] == 'сумма вашей задолженности составляет' and len(all_buyers_documents[0])>0:
            debts_buyers += [{'name':all_buyers_documents[0][0]['name'],'message':summa_sverki_buyers[0], 'summa':summa_sverki_buyers[1]}]
            pass

    return debts_buyers
    pass


list_sverok = get_hvosty_lists(cur,start_data,ending_data)



summs_lists = [i['summa'] for i in list_sverok] 
names_lists = [i['name'] for i in list_sverok] 


#-----------------EXCELL!!!!!!!!!!!!!!!1-------

#https://habrahabr.ru/post/99923/
#https://habrahabr.ru/post/232291/
#https://habrahabr.ru/company/otus/blog/331998/



Excel = win32com.client.Dispatch("Excel.Application")
#wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart.xls')
wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart_2016.xls')
#wb = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\test_dbf\\dipart_train.xls')
sheet = wb.ActiveSheet


def nuts(some_list, col_name):
    cell_number = 1
    for rec in some_list:
        sheet.Cells(1,col_name).value = "Задолженность поставщиков"
        sheet.Cells(cell_number,col_name).value = rec
        cell_number = cell_number + 1    
        pass
    pass                


#nuts(summs_lists,2)
#nuts(names_lists,1)


#сохраняем рабочую книгу
wb.Save()

#закрываем ее
wb.Close()

#закрываем COM объект
Excel.Quit()
"""
"""
def get_hvosty_lists(cursor,data_start, data_end):
    contragents_id = create_list_of_table_values(cursor.execute(select_contragents_identificator),cursor.description)

    debts_providers=[]
    prepayment_providers=[]
    debts_buyers=[]
    prepayment_buyers=[]

    contargents_id_list = [i['id'] for i in contragents_id]

    for altair in contargents_id_list:
        select_documents_providers = [select_docs_prodanoe.format(doc_two, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc_two in (tn_buyers,pp_buyers)]
        select_documents_buyers = [select_docs_poluchenoe.format(doc, "'"+str(altair)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (tn,pp)]

        

        all_buyers_documents = [create_list_of_table_values(cursor.execute(table_two),cursor.description) for table_two in select_documents_buyers]
        all_providers_documents = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents_providers]

        summa_sverki_providers = get_pays_balance(all_buyers_documents[1], all_buyers_documents[0], 'summ')
        summa_sverki_buyers = get_pays_balance(all_providers_documents[1], all_providers_documents[0], 'summ')


        if summa_sverki_providers[0] != 'Задолженности нет!' and  summa_sverki_providers[0] =='сумма задолженности контрагента составляет' and len(all_providers_documents[0])>0:
            debts_providers += [{'name':all_providers_documents[0][0]['name'],'message':summa_sverki_providers[0], 'summa':summa_sverki_providers[1]}]
            pass
        
        if summa_sverki_providers[0]  != 'Задолженности нет!' and  summa_sverki_providers[0] =='сумма вашей задолженности составляет' and len(all_providers_documents[0])>0:
            prepayment_providers += [{'name':all_providers_documents[0][0]['name'], 'message':summa_sverki_providers[0], 'summa':summa_sverki_providers[1]}]
            pass

        if summa_sverki_buyers[0] != 'Задолженности нет!' and summa_sverki_buyers[0] == 'сумма задолженности контрагента составляет' and len(all_buyers_documents[0])>0:
            debts_buyers += [{'name':all_buyers_documents[0][0]['name'],'message':summa_sverki_buyers[0], 'summa':summa_sverki_buyers[1]}]
            pass

        if summa_sverki_buyers[0]  != 'Задолженности нет!' and summa_sverki_buyers[0] =='сумма вашей задолженности составляет' and len(all_buyers_documents[0])>0:
            prepayment_buyers += [{'name':all_buyers_documents[0][0]['name'],'message':summa_sverki_buyers[0], 'summa':summa_sverki_buyers[1]}]
            pass
    return(debts_providers,prepayment_providers,debts_buyers,prepayment_buyers)
    pass


list_sverok = get_hvosty_lists(cur,start_data,ending_data)



summs_lists = [[i['summa'] for i in list_sverok[l]] for l in (0,1,2,3)]
names_lists = [[i['name'] for i in list_sverok[l]] for l in (0,1,2,3)]

debts_providers_sums = summs_lists[0]
prepayment_providers_sums = summs_lists[1]
debts_buyers_sums = summs_lists[2]
prepayment_buyers_sums = summs_lists[3]

debts_providers_names = names_lists[0]
prepayment_providers_names = names_lists[1]
debts_buyers_names = names_lists[2]
prepayment_buyers_names = names_lists[3]

#-----------------EXCELL!!!!!!!!!!!!!!!1-------

#https://habrahabr.ru/post/99923/
#https://habrahabr.ru/post/232291/
#https://habrahabr.ru/company/otus/blog/331998/



Excel = win32com.client.Dispatch("Excel.Application")
#wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart.xls')
wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart_2016.xls')
#wb = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\test_dbf\\dipart_train.xls')
sheet = wb.ActiveSheet


def nuts(some_list,some_list1,some_list2,some_list3, col_name):
    cell_number = 1
    for rec in some_list:
        sheet.Cells(1,col_name).value = "Задолженность поставщиков"
        sheet.Cells(cell_number,col_name).value = rec
        cell_number = cell_number + 1    
        pass
        

    cell_number1 = len(some_list)+5
    sheet.Cells(cell_number1-2,col_name).value = "Предоплата поставщикам"
    for rec1 in some_list1:
        sheet.Cells(cell_number1,col_name).value = rec1
        cell_number1 = cell_number1 + 1    
        pass


    cell_number2 = (len(some_list1)+5+len(some_list)+5)
    sheet.Cells(cell_number2-2,col_name).value = "Задолженность покупателей"
    for rec2 in some_list2:
        sheet.Cells(cell_number2,col_name).value = rec2
        cell_number2 = cell_number2 + 1    
        pass


    cell_number3 = (len(some_list)+5+len(some_list1)+5+len(some_list2)+5)
    sheet.Cells(cell_number3-2,col_name).value = "Предоплата от покупателей"

    for rec3 in some_list3:
        sheet.Cells(cell_number3,col_name).value = rec3
        cell_number3 = cell_number3 + 1    
        pass                


nuts(debts_providers_sums,prepayment_providers_sums,debts_buyers_sums,prepayment_buyers_sums,2)
nuts(debts_providers_names,prepayment_providers_names,debts_buyers_names,prepayment_buyers_names,1)


#сохраняем рабочую книгу
wb.Save()

#закрываем ее
wb.Close()

#закрываем COM объект
Excel.Quit()
"""