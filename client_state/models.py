#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.db import migrations, models
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from itertools import groupby
from collections import defaultdict
from operator import itemgetter

import datetime
from datetime import date
import os
import sqlite3

import itertools
import requests
import openpyxl
from openpyxl import load_workbook,Workbook


from TESTO import nbrb_rates_today, nbrb_rates_on_date, rates, years, months, days
from TESTO import create_list_of_table_values, sum_of_list, return_excel_list, generate_data_list
from TESTO import outcome_serv_nds, outcome_tn_nds, income_serv_nds, income_tn_nds, select_course_on_date, income_tovary,outcome_full_nonds,select_course_data, insert_courses


from . import sql_commands as sq_c



BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
TO_BASE_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'
TO_DOCS_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'+'media'+'\\'+'docs'+'\\'


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
                       'nds':round(sum([float(x['nds']) for x in i]),2)}]

    return output_list
    pass

def grouping_by_key(income_list, key_name):
    output_list = []
    full_grouped_list = []

    sorted_list = sorted(income_list, key=itemgetter(key_name))

    for key, group in itertools.groupby(sorted_list, key=lambda x:x[key_name]):
        grouped_sorted_list = list(group)
        full_grouped_list += [grouped_sorted_list]                              

    return full_grouped_list
    pass

 
#---------------------------------CURENT FIN STATE---------------------------------#

class CompanyBalance:
    def __init__(self, base_name = None, data_start = None, data_end = None):
        self.base_name = base_name
        self.data_start = data_start
        self.data_end = data_end


    def tax_sum(self, select_command, cursor, tax_type):
        return sum([float(x[tax_type]) for x in create_list_of_table_values(cursor.execute(select_command.format(self.data_start, self.data_end)),cursor.description) if x[tax_type] != None])


    def count_nds(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        outcome_nds_sum = self.tax_sum(outcome_serv_nds, cur, 'nds')+self.tax_sum(outcome_tn_nds, cur, 'nds')
        income_nds_sum = self.tax_sum(income_serv_nds, cur, 'nds')+self.tax_sum(income_tn_nds, cur, 'nds')+self.tax_sum(income_tovary, cur, 'nds')
 
        conn.commit()
        conn.close()        

        return (outcome_nds_sum, income_nds_sum, outcome_nds_sum - income_nds_sum)
        pass


    def count_usn(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        usn_sum = round(self.tax_sum(outcome_full_nonds, cur, 'summ')*0.05, 2)
 
        conn.commit()
        conn.close()

        return usn_sum
        pass


    def create_tax_excel(request, income_list, tax_type):
        output_doc = BASE_DIR+'\\'+"tax_result.xlsx"
        openpyxl.Workbook().save(output_doc)
        output_list = load_workbook(output_doc,data_only = True)
        main_out_sheet = output_list.active    

        def insert_cell(row_val, col_val, cell_value):
            main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
            pass


        if tax_type == "nds":
            insert_cell(1, 1, "НДС за выбранный период составляет")
            insert_cell(2, 1, "Входящий НДС")
            insert_cell(3, 1, "Исходящий НДС")
            insert_cell(4, 1, "НДС к уплате:")
            insert_cell(2, 2, str(round(income_list[0],2))+" "+"руб.")
            insert_cell(3, 2, str(round(income_list[1],2))+" "+"руб.")
            insert_cell(4, 2, str(round(income_list[2],2))+" "+"руб.")

        
        else: 
            insert_cell(1, 1, "УСН за выбранный период составляет")  
            insert_cell(1, 2, str(round(income_list,2))+" "+"руб.") 


        output_list.save(filename = output_doc)

        return(str(output_doc))
        pass


#---------------------------------HVOSTY---------------------------------#

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





#------------------------SVERKA SS PORTALOM--------------------



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


def get_today_course():
    courses_list = []
    for i in [requests.get(nbrb_rates_today.format(x['code_nbrb'])).json() for x in  rates]:
        courses_list += [{"cur_name":i["Cur_Name"],"cur_scale":i["Cur_Scale"],"cur_rate":i["Cur_OfficialRate"] }]
    return courses_list
    pass


class CurrencyStat:
    def __init__(self, 
                select_command=sq_c.select_curr_income, 
                data_start="2018-05-11", 
                data_end="2018-05-15", 
                base_name = "zeno.sqlite",
                request_type = "исходящий",):

       self.select_command = select_command
       self.data_start = data_start
       self.data_end = data_end
       self.base_name = base_name
       self.request_type = request_type

    def create_rates_list(self, select_curr):
        conn = sqlite3.connect(TO_BASE_PATH+'sqlite_bases'+'\\'+'courses.sqlite')
        cur = conn.cursor()
        sql_request = select_curr.format("'"+str(self.data_start)+"'", "'"+str(self.data_end)+"'")
        return create_list_of_table_values(cur.execute(sql_request),cur.description)
        pass


    def transform_sql_to_list(self):
        conn = sqlite3.connect(self.base_name)
        cur = conn.cursor()
        if self.request_type == 'входящий':
            sel_request = sq_c.select_curr_income
        if self.request_type == 'исходящий':
            sel_request = sq_c.select_curr_outcome

        sql_request = sel_request.format("'"+self.data_start+"'","'"+self.data_end+"'")
    
        return create_list_of_table_values(cur.execute(sql_request),cur.description)
        pass

    def result(self):
        eur = []
        usd = []
        rub = []

        for x in self.transform_sql_to_list():
            if x['currency_type'] == '3':
                for y in self.create_rates_list(sq_c.select_eur_course):
                    for i in self.create_rates_list(sq_c.select_usd_course):
                        if x['doc_date'] == y['data'] and x['doc_date']== i['data'] and x['name'] != None and type(x['name']) != None:
                            eur += [{
                                    'doc': x['document_name'],  
                                    'date' : x['doc_date'], 
                                    'contragent':x['contragent_name'],
                                    'country': x['name'], 
                                    'summ':x['summ'], 
                                    'rate_on_date':y['rate'],
                                    'usd_rate_on_date':i['rate'],
                                    'bel_sum':round(float(x['summ'])*float(y['rate']),3),
                                    'usd_sum':round(float(x['summ'])*float(y['rate'])/float(i['rate']),3),
                                    'curr_name':'EUR',
                                    }]

            if x['currency_type'] == '7':
                for y in self.create_rates_list(sq_c.select_usd_course):
                    for i in self.create_rates_list(sq_c.select_usd_course):
                        if x['doc_date'] == y['data'] and x['doc_date']== i['data'] and x['name'] != None and type(x['name']) != None:
                            usd += [{
                                    'doc': x['document_name'],  
                                    'date' : x['doc_date'], 
                                    'contragent':x['contragent_name'],
                                    'country': x['name'], 
                                    'summ':x['summ'], 
                                    'rate_on_date':y['rate'],
                                    'usd_rate_on_date':i['rate'],
                                    'bel_sum':round(float(x['summ'])*float(y['rate']),3),
                                    'usd_sum':round(float(x['summ'])*float(y['rate'])/float(i['rate']),3),
                                    'curr_name':'USD',
                                    }]


            if x['currency_type'] == '6':
                for y in self.create_rates_list(sq_c.select_rus_course):
                    for i in self.create_rates_list(sq_c.select_usd_course):
                        if x['doc_date'] == y['data'] and x['doc_date']== i['data'] and x['name'] != None  and type(x['name']) != None:
                            rub += [{
                                    'doc': x['document_name'],  
                                    'date' : x['doc_date'], 
                                    'contragent':x['contragent_name'], 
                                    'country': x['name'], 
                                    'summ':x['summ'], 
                                    'rate_on_date':y['rate'],
                                    'usd_rate_on_date':i['rate'],
                                    'bel_sum':round(float(x['summ'])*float(y['rate']/float(y['scale'])),3),
                                    'usd_sum':round(float(x['summ'])*float(y['rate']/float(y['scale'])),3)/float(i['rate']),
                                    'curr_name':'RUB',
                                    }]
        return (eur, usd, rub)
        pass


    def stat_for_country(self):
        state_for_cuntry = []
        
        for x in grouping_by_key(self.result()[0]+self.result()[1]+self.result()[2], 'country'):
            state_for_cuntry+=[{
                    'country':x[0]['country'],
                    'summ':round(sum([float(n['summ']) for n in  x]),2),
                    'bel_sum':round(sum([float(n['bel_sum']) for n in  x]),2),
                    'usd_sum':round(sum([float(n['usd_sum']) for n in  x]),2),
                    }]
        return state_for_cuntry
        pass



    def final_grouping(self):
        list_of_lists = []
        final = []
        for count in self.result():
            for i in grouping_by_key(count, 'country'):
                for x in grouping_by_key(i, 'date'):
                    final+=[{
                    'date':x[0]['date'],
                    'contragent':x[0]['contragent'],
                    'country':x[0]['country'],
                    'summ':round(sum([float(n['summ']) for n in  x]),2),
                    'rate_on_date':x[0]['rate_on_date'],
                    'usd_rate_on_date':x[0]['usd_rate_on_date'],
                    'bel_sum':round(sum([float(n['bel_sum']) for n in  x]),2),
                    'usd_sum':round(sum([float(n['usd_sum']) for n in  x]),2),
                    'curr_name':x[0]['curr_name'],
                    }]
            list_of_lists+=[final]

        return list_of_lists
        pass


    def create_statistica_excel(self):
        output_doc = BASE_DIR+"result.xlsx"
        openpyxl.Workbook().save(output_doc)
        output_list = load_workbook(output_doc,data_only = True)
        main_out_sheet = output_list.active
        output_list.create_sheet("full_stat")
        full_stat = output_list["full_stat"]


        income_list = self.final_grouping()
        income_list_main = self.stat_for_country()

        def insert_cell(row_val, col_val, cell_value):
            full_stat.cell(row = row_val, column = col_val).value = cell_value
            pass  


        def insert_cell_main(row_val, col_val, cell_value):
            main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
            pass 



        col_names = ["Дата", "Контрагент", "Страна","Валюта", "Сумма в валюте", "Сумма в бел. рублях",  "Сумма в долларах", "Курс валюты на дату", "Курс доллара на дату"]    
        insert_cell(1, 1, "Дата")
        
        for name in col_names:
            insert_cell(1, col_names.index(name), name)

        for contr_name in col_names[0:4]:
            insert_cell(1, col_names.index(name), name)


        for i in range(len(income_list_main)):
            insert_cell_main(i+3, 1, income_list_main[i]['country'])
            insert_cell_main(i+3, 2, income_list_main[i]['summ'])
            insert_cell_main(i+3, 3, income_list_main[i]['bel_sum'])
            insert_cell_main(i+3, 4, income_list_main[i]['usd_sum'])


    
        for i in range(len(income_list[0])):
            insert_cell(i+3, 1, income_list[0][i]['date'])
            insert_cell(i+3, 2, income_list[0][i]['contragent'])
            insert_cell(i+3, 3, income_list[0][i]['country'])
            insert_cell(i+3, 4, income_list[0][i]['curr_name'])
            insert_cell(i+3, 5, income_list[0][i]['summ'])
            insert_cell(i+3, 6, income_list[0][i]['bel_sum'])
            insert_cell(i+3, 7, income_list[0][i]['usd_sum'])
            insert_cell(i+3, 8, income_list[0][i]['rate_on_date'])
            insert_cell(i+3, 9, income_list[0][i]['usd_rate_on_date'])

        output_list.save(filename = output_doc)
        return(str(output_doc))
        pass




##################----------COURSES--------------##########

class CoursesUpdater:

    def today_updater(self):
        conn = sqlite3.connect('courses.sqlite')
        cur = conn.cursor()
        today_course = []
        for val in rates:
            today_course +=  create_list_of_table_values(cur.execute(select_course_on_date.format(val['name'], "'"+str(date.today())+"'")),cur.description)

        datas_table = create_list_of_table_values(cur.execute(select_course_data.format('usd')),cur.description)
        for i in range(len(rates)):
            datas_table = create_list_of_table_values(cur.execute(select_course_data.format(rates[i]['name'])),cur.description)
            if str(date.today()) != datas_table[-1]['data']:
                cur.executemany(insert_courses.format(rates[i]['name']),  [(str(date.today()), get_today_course()[i]['cur_name'],get_today_course()[i]['cur_scale'],get_today_course()[i]['cur_rate'])])    
        conn.commit()
        conn.close()
        return today_course
        pass


#---------------------------------STATISTIKA End----------------



class Upload_file(models.Model):
    uploaded_file = models.FileField(upload_to='docs/')
    start_year = models.CharField(max_length=350, choices=years,db_index=True, blank = True)
    start_month = models.CharField(max_length=350, choices=months,db_index=True, blank = True)
    start_day = models.CharField(max_length=350, choices=days,db_index=True, blank = True)

    end_year = models.CharField(max_length=350, choices=years,db_index=True, blank = True)
    end_month = models.CharField(max_length=350, choices=months,db_index=True, blank = True)
    end_day = models.CharField(max_length=350, choices=days,db_index=True, blank = True)




