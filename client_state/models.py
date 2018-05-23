#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.db import migrations, models
from itertools import groupby
from collections import defaultdict
from operator import itemgetter
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import datetime
from datetime import date
import os
import sqlite3
import mimetypes

import itertools
import requests
import openpyxl
from openpyxl import load_workbook,Workbook

from . import sql_commands as sq_c
from . import variables as var



BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
TO_BASE_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'
TO_DOCS_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'+'media'+'\\'+'docs'+'\\'

def sum_result(income_list):
    return round(sum([i['nds'] for i in income_list if i['full_sum'] != None]),2)


def sum_of_list(sum_name,income_list):
    return sum([x[sum_name] for x in income_list])
    pass


def create_sorted_list(income_list):
    output_list = []
    full_grouped_list = []

    sorted_list = sorted(income_list, key=itemgetter('name'))

    for key, group in itertools.groupby(sorted_list, key=lambda x:x['name']):
        grouped_sorted_list = list(group)
        full_grouped_list += [grouped_sorted_list]                              

    for i in full_grouped_list:
        output_list+=[{'name': i[0]['name'],
                       'unp':str(i[0]['unp']), 
                       'nds':round(sum([x['nds'] for x in i]),2)}]

    return output_list
    pass


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



def curent_finace_states(start, end, cursor, nalog_system):
    from_providers = transform_sql_to_list(cursor, sq_c.select_docs_from_providers, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
    to_buyers = transform_sql_to_list(cursor, sq_c.select_docs_to_buyers, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_ishod_nds_usl = transform_sql_to_list(cursor, sq_c.sel_usl_with_ishod_nds, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )
    list_ishod_nds_tn = transform_sql_to_list(cursor, sq_c.sel_tn_with_ishod_nds, sq_c.tn_providers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_vhod_nds_usl = transform_sql_to_list(cursor, sq_c.sel_vhod_usl_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
    list_vhod_nds_tn = transform_sql_to_list(cursor, sq_c.sel_vhod_tn_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )

    list_tovary_nds  = transform_sql_to_list(cursor, sq_c.sel_tovary_with_vhod_nds,   "'"+start+"'",  "'"+str(end)+"'" )


    full_vhod_nds = sum_result(list_vhod_nds_usl)+sum_result(list_vhod_nds_tn)+sum_result(list_tovary_nds)
    full_ishod_nds = sum_result(list_ishod_nds_usl)+sum_result(list_ishod_nds_tn)


    unsorted_full_list_vhod = [i for i in list_tovary_nds+list_vhod_nds_tn+list_vhod_nds_usl if i['nds'] != 0.0 and i['nds']!=None]
    unsorted_full_list_ishod = [i for i in list_ishod_nds_tn+list_ishod_nds_usl if i['nds'] != 0.0 and i['nds']!=None]
    
    list_vhod = create_sorted_list(unsorted_full_list_vhod)
    list_ishod = create_sorted_list(unsorted_full_list_ishod)


    if nalog_system == 'nds':
        now_fin_states = str(round(full_ishod_nds - full_vhod_nds,2))
        tax_system = 'nds' 
    else:
        now_fin_states = str(round(sum([i['summ'] for i in to_buyers])*0.05,2))
        tax_system = 'usn' 


    return(tax_system, full_vhod_nds, full_ishod_nds, now_fin_states, list_ishod, list_vhod)
    pass



def transform_sql(select_command,docs,pays,cursor,contragent,data_start,data_end):
    select_documents = [select_command.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") for doc in (docs,pays)]
    documents_list = [create_list_of_table_values(cursor.execute(table),cursor.description) for table in select_documents]

    summa_tn = sum([i['summ']for i in documents_list[0]])
    summa_pp = sum([i['summ']for i in documents_list[1]])
    
    return (documents_list,summa_tn,summa_pp)
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




def create_hvosty_excel(request, income_list):
    output_doc = BASE_DIR+'\\'+"resultat.xlsx"
    openpyxl.Workbook().save(output_doc)
    output_list = load_workbook(output_doc,data_only = True)
    main_out_sheet = output_list.active


    def insert_cell(row_val, col_val, cell_value):
        main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
        pass

    insert_cell(1, 1, "Контрагент")
    insert_cell(1, 2, "Сумма")

    insert_cell(3, 1, 'ЗАДОЛЖЕННОСТЬ ПОКУПАТЕЛЕЙ (Д 62)'  )
    for i in range(len(income_list[0])):
        insert_cell(i+5, 1, income_list[0][i]['name'] )
        insert_cell(i+5, 2, income_list[0][i]['summa'])


    insert_cell(len(income_list[0])+10, 1, 'АВАНСЫ ПОКУПАТЕЛЕЙ (КР 62)'  )
    for i in range(len(income_list[1])):
        insert_cell(i+len(income_list[0])+12, 1, income_list[1][i]['name'] )
        insert_cell(i+len(income_list[0])+12, 2, income_list[1][i]['summa'] )    

    insert_cell(len(income_list[0])+len(income_list[1])+16, 1, 'АВАНСЫ ПОСТАВЩИКАМ(Д 60)' )
    for i in range(len(income_list[2])):
        insert_cell(i+len(income_list[0])+len(income_list[1])+18, 1, income_list[2][i]['name'] )
        insert_cell(i+len(income_list[0])+len(income_list[1])+18, 2, income_list[2][i]['summa'] )  
    
    insert_cell(len(income_list[0])+len(income_list[1])+len(income_list[2])+22, 1, 'ЗАДОЛЖЕННОСТЬ ПЕРЕД ПОСТАВЩИКАМИ(КР 60)' )
    for i in range(len(income_list[3])):
        insert_cell(i+len(income_list[0])+len(income_list[1])+len(income_list[2])+24, 1, income_list[3][i]['name'] )
        insert_cell(i+len(income_list[0])+len(income_list[1])+len(income_list[2])+24, 2, income_list[3][i]['summa'] ) 
    
    output_list.save(filename = output_doc)

    return(str(output_doc))
    pass




def create_tax_excel(request, income_list):
    output_doc = BASE_DIR+'\\'+"tax_result.xlsx"
    openpyxl.Workbook().save(output_doc)
    output_list = load_workbook(output_doc,data_only = True)
    main_out_sheet = output_list.active    

    def insert_cell(row_val, col_val, cell_value):
        main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
        pass


    if income_list[0] == "nds":
        insert_cell(1, 1, income_list[0]+" "+"за выбранный период составляет")
        insert_cell(2, 1, "Входящий" +" "+income_list[0])
        insert_cell(3, 1, "Исходящий"+" "+income_list[0])
        insert_cell(4, 1, income_list[0]+" "+"К уплате:")
        insert_cell(1, 2, income_list[0])
        insert_cell(2, 2, str(round(income_list[1],2))+" "+"руб.")
        insert_cell(3, 2, str(round(income_list[2],2))+" "+"руб.")
        insert_cell(4, 2, str(income_list[3])+" "+"руб.")
    else: 
        insert_cell(1, 1, income_list[0]+" "+"за выбранный период составляет")  
        insert_cell(1, 2, income_list[3]+" "+"руб.") 


    output_list.save(filename = output_doc)

    return(str(output_doc))
    pass    




def return_excel_list(income_file, client_name, doc_type):
    fp = open(income_file, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(income_file)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(income_file).st_size)
    response['Content-Disposition'] = "attachment; filename = {}-{}.xlsx".format(client_name,doc_type)
    os.remove(income_file)
    return response







#ВХОДЯЩИЙ:
data_type = 'income'
unp_number = 2
name_col = 4
list_number = 5


#ИСХОДЯЩИЙ
#data_type = 'outcome'
#unp_number = 9
#name_col = 11
#list_number = 0


output_doc = BASE_DIR+'\\'+"result_{}.xlsx".format(data_type)
openpyxl.Workbook().save(output_doc)

output_list = load_workbook(output_doc,data_only = True)
main_out_sheet = output_list.active




def get_eschf_data(main_inner_sheet):
    first_list_from_excel =[]

    for x in range(1, 8):
        if main_inner_sheet.cell(row=x, column=1).value == "Код страны поставщика": 
            start_point = x+1

    for i in range(start_point, main_inner_sheet.max_row+1):
        if  main_inner_sheet.cell(row=i, column=18).value != "Аннулирован": 
            if main_inner_sheet.cell(row=i, column=unp_number).value != None: 
                first_list_from_excel += [{ 
                        "unp" : main_inner_sheet.cell(row=i, column=unp_number).value, 
                        "name" : main_inner_sheet.cell(row=i, column=name_col).value,
                        "nds" : main_inner_sheet.cell(row=i, column=42).value,
                        }]
    return create_sorted_list(first_list_from_excel)
    pass




def find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system):
    connect = sqlite3.connect(sql_base_name )
    cursor = connect.cursor()
    not_in_excel = get_eschf_data(main_inner_sheet)
    not_in_base = curent_finace_states(data_start, data_end, cursor,nalog_system)[list_number]


    for i in curent_finace_states(data_start, data_end, cursor, nalog_system)[list_number]:
        for x in get_eschf_data(main_inner_sheet):
            if i['unp'] == x['unp'] and i['nds'] == x['nds']:
                not_in_excel.remove(x)
                not_in_base.remove(i)
                        
    connect.commit()
    connect.close()
    return(not_in_excel,not_in_base)
    pass




def insert_into_excel(request, excel_income, base_name, data_start, data_end, nalog_system):
    portal_list = load_workbook(TO_DOCS_PATH+excel_income,data_only = True)
    main_inner_sheet = portal_list.active
    sql_base_name = TO_BASE_PATH+base_name+'.sqlite'


    connect = sqlite3.connect(sql_base_name)
    cursor = connect.cursor()

    def insert_cell(row_val, col_val, cell_value):
        main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
        pass

    for x in (1,4):
        insert_cell(3, x, "Контрагент")

    for i in (2,5):
        insert_cell(3, i, "НДС")    

    insert_cell(1, 4, "Есть в базе, нет на портале")
    insert_cell(1, 1, "Есть на портале, нет в базе")

    insert_cell(2, 4, "Весь НДС из базы")
    insert_cell(2, 1, "Весь НДС с Портала")


    insert_cell(2, 5, sum_of_list('nds',curent_finace_states(data_start, data_end, cursor, nalog_system)[list_number]))
    insert_cell(2, 2, sum_of_list('nds', get_eschf_data(main_inner_sheet)))

    for i in range(len(find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[0])):
        insert_cell(i+5, 1, find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[0][i]['name'])
        insert_cell(i+5, 2, find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[0][i]['nds'])

    for i in range(len(find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[1])):

        insert_cell(i+5, 4, find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[1][i]['name'])
        insert_cell(i+5, 5, find_difference(main_inner_sheet, sql_base_name, data_start, data_end, nalog_system)[1][i]['nds'])

    output_list.save(filename = output_doc)
    connect.commit()
    connect.close()
    return(str(output_doc))
    pass













#-------STATISTICA-----------------------------


nbrb_rates_today = "http://www.nbrb.by/API/ExRates/Rates/{}"
nbrb_rates_on_date = "http://www.nbrb.by/API/ExRates/Rates/{}?onDate={}"


rates = [
{'name':'grivna',"code_nbrb": 290, 'request':sq_c.select_grivn_course, 'base_id': '4'}, 
{'name': "usd","code_nbrb": 145, 'request':sq_c.select_usd_course, 'base_id': '7'}, 
{'name': "eur","code_nbrb": 292, 'request':sq_c.select_eur_course, 'base_id': '3'},
{'name': "rus","code_nbrb": 298, 'request':sq_c.select_rus_course, 'base_id': '6'}
]




def generate_data_list(start_data, end_data):
    start = datetime.datetime.strptime(start_data, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_data, "%Y-%m-%d")
    return [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    pass


def get_today_course(addres):
    courses_list = []
    for i in [requests.get(addres.format(x['code_nbrb'])).json() for x in  rates]:
        courses_list += [{"cur_name":i["Cur_Name"],"cur_scale":i["Cur_Scale"],"cur_rate":i["Cur_OfficialRate"] }]
    return courses_list
    pass


def create_courses_table(addres, money):
    courses_list = []

    for i in [requests.get(addres.format(money, data.strftime("%Y-%m-%d"))).json() for data in  generate_data_list("2018-01-01", str(date.today()))]:
        courses_list += [( str(i["Date"][:10]),i["Cur_Name"], i["Cur_Scale"], i["Cur_OfficialRate"] )]
    return courses_list
    pass


def update_courses_base(table, income_list):
    conn = sqlite3.connect('courses.sqlite')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table['name'], courses_colls))
    cur.executemany(insert_courses.format(table['name']), income_list)
    conn.commit()
    conn.close()
    pass



def valuty_sql_to_list(base_name, select_comand, data_start, data_end):
    conn = sqlite3.connect(base_name)
    cur = conn.cursor()
    sql_request = select_comand.format(data_start, data_end)

    return create_list_of_table_values(cur.execute(sql_request),cur.description)
    pass



def currency_docs_counter(data_start, data_end, base_name):
    count =[]
    for i in valuty_sql_to_list(base_name, sq_c.select_valuty_income, data_start, "'"+data_end+"'"):
        if i['doc_date'] >= data_start and i['doc_date'] <= data_end:
            count+=[{'date':i['doc_date'], 'document': i['document_name'], 'summ': i['summ'],'contragent':i['contragent_name'], 'currency_type':i['currency_type'], }]
    return count
    pass



def statistika(currency, data_start, data_end, base_name):
    result = []
    for x in currency_docs_counter(data_start, data_end, base_name):
        for y in valuty_sql_to_list('courses.sqlite', currency['request'], "'"+data_start+"'", "'"+data_end+"'" ):
            if y['data'] == x['date']:
                if x['currency_type'] == currency['base_id']:
                    result +=  [{
                                'контрагент':x['contragent'],
                                'дата': y['data'],
                                'курс на дату документа':y['rate'], 
                                'сумма в рублях':x['summ'],
                                'дата': y['data']
                                }]
    return result
    pass     




def return_final_statistica(data_start, data_end, base_name):
    final_list = []
    for x in range(len(rates)):
        final_list += [statistika(rates[x],data_start, data_end, base_name)]
    return final_list    






class Proba:
    def __init__(self, select_command=sq_c.select_valuty_income, 
        data_start="2018-05-11", 
        data_end="2018-05-12", 
        base_name = "zeno.sqlite"):

       self.select_command = select_command
       self.data_start = data_start
       self.data_end = data_end
       self.base_name = base_name

    def valuty_sql_to_l(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        sql_request = self.select_command.format(self.data_start, self.data_end)

        return create_list_of_table_values(cur.execute(sql_request),cur.description)
        pass

    def currency_docs_counter_(self):
        count =[]
        for i in self.valuty_sql_to_l():
            if i['doc_date'] >= self.data_start and i['doc_date'] <= self.data_end:
                count+=[{'date':i['doc_date'], 'document': i['document_name'], 'summ': i['summ'],'contragent':i['contragent_name'], 'currency_type':i['currency_type'], }]
        return count
        pass


    def create_rates_list(self):
        conn = sqlite3.connect(TO_BASE_PATH+'sqlite_bases'+'\\'+'courses.sqlite')
        cur = conn.cursor()
        sql_request = sq_c.select_eur_course.format("'"+str(self.data_start)+"'", "'"+str(self.data_end)+"'")
        return create_list_of_table_values(cur.execute(sq_c.select_eur_course),cur.description)
        pass
































def create_statistica_excel(request, base_name, data_start, data_end):
    output_doc = BASE_DIR+"tax_result.xlsx"
    openpyxl.Workbook().save(output_doc)
    output_list = load_workbook(output_doc,data_only = True)
    main_out_sheet = output_list.active  


    income_list = return_final_statistica(data_start, data_end, base_name)


    def insert_cell(row_val, col_val, cell_value):
        main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
        pass  

    insert_cell(1, 1, "Дата")
    insert_cell(1, 2, "Контрагент")
    insert_cell(1, 3, "Валюта")
    insert_cell(1, 3, "Страна")
    insert_cell(1, 4, "Сумма в валюте")
    insert_cell(1, 5, "Сумма в бел. рублях")


    
    for i in range(len(income_list[0])):
        insert_cell(i+3, 1, income_list[0][i]['дата'])
        insert_cell(i+3, 2, income_list[0][i]['контрагент'])
        insert_cell(i+3, 3, income_list[0][i]['курс на дату документа'])
        insert_cell(i+3, 4, income_list[0][i]['сумма в рублях'])


        output_list.save(filename = output_doc)
    return(str(output_doc))
    pass









#---------------------------------STATISTIKA End----------------











years = [("2018", "2018"),("2017", "2017"),("2016", "2016"), ("2015", "2015"),]


months = [ ("01", "январь", ),("02", "февраль", ),("03",  "март"),( "04","апрель"),("05", "май" ), ("06","июнь"),
            ("07", "июль"),("08", "август"),("09", "сентябрь"), ("10", "октябрь"),("11", "ноябрь"),
            ("12", "декабрь")]



days = [("01","01"), ("02","02"), ("03","03"), ("04","04"), ("05","05"), ("06","06"), ("07","07"), 
        ("08","08"), ("09","09"), ("10","10"), ("11","11"), ("12","12"), ("13","13"),  
        ("14","14"), ("15","15"), ("16","16"), ("17","17"), ("18","18"), ("19","19"),
        ("20","20"), ("21","21"), ("22","22"), ("23","23"), ("24","24"), ("25","25"), 
        ("26","26"),  ("27","27"),("28","28"), ("29","29"),  ("30","30"),  ("31", "31"), ]



class Upload_file(models.Model):
    uploaded_file = models.FileField(upload_to='docs/')
    start_year = models.CharField(max_length=350, choices=years,db_index=True, blank = True)
    start_month = models.CharField(max_length=350, choices=months,db_index=True, blank = True)
    start_day = models.CharField(max_length=350, choices=days,db_index=True, blank = True)

    end_year = models.CharField(max_length=350, choices=years,db_index=True, blank = True)
    end_month = models.CharField(max_length=350, choices=months,db_index=True, blank = True)
    end_day = models.CharField(max_length=350, choices=days,db_index=True, blank = True)




