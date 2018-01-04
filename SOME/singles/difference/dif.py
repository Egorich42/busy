#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt

import sqlite3

import sql_commands as sq_c
import variables as var

from functools import reduce


conn = sqlite3.connect('avangard.sqlite')
cur = conn.cursor()

Excel = win32com.client.Dispatch("Excel.Application")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

first_list = Excel.Workbooks.Open(BASE_DIR+'avangard_in_min.xls')
first_dataset = first_list.ActiveSheet


def find_first_point(dataset):
	for i in range(1,10):
		if dataset.Cells(i,1).value != None and dataset.Cells(i,1).value == 'Код страны поставщика':
			dataset.Cells(i,1).value
			return i+1
			pass

def find_endpoint(dataset,start):
	for i in range(start,510):
		if dataset.Cells(i,1).value == None:
			return i-1
			pass


start_point = find_first_point(first_dataset)
endpoint = find_endpoint(first_dataset,start_point)
interval = "{}"+str(start_point)+":"+"{}"+str(endpoint)

def excol_to_list(dataset_name, col_name):
	list_name = [r[0].value for r in dataset_name.Range(interval.format(col_name,col_name))]
	return list_name
	pass



def get_from_base(select_command,doc,cursor,contragent,data_start,data_end):
    select_documents = select_command.format(doc, "'"+str(contragent)+"'", "'"+data_start+"'","'"+data_end+"'") 
    documents_list = var.create_list_of_table_values(cursor.execute(select_documents),cursor.description)
    return documents_list
    pass
    


def get_docs_lists(cursor,data_start, data_end):
    docum = []
    contragents_id = var.create_list_of_table_values(cursor.execute(sq_c.select_contragents_identificator),cursor.description)
    contargents_id_list = [i['id'] for i in contragents_id]
    
    for altair in contargents_id_list:
        providers_docs = get_from_base(sq_c.select_documents_to_buyers,sq_c.tn_buyers,cursor,altair,data_start,data_end)
        if providers_docs != []:
        	docum += [providers_docs]
    return docum
    pass


country_code = excol_to_list(first_dataset,"A")
provider_unp= excol_to_list(first_dataset,"B")
provider_name = excol_to_list(first_dataset,"D")

eschf_number = excol_to_list(first_dataset,"N")
eschf_type = excol_to_list(first_dataset,"P")
eschf_status = excol_to_list(first_dataset,"Q")

expose_date = excol_to_list(first_dataset,"R")
sovershenia_date = excol_to_list(first_dataset,"S")
sign_date = excol_to_list(first_dataset,"T")
to_zero_date = excol_to_list(first_dataset,"U")

contract_number = excol_to_list(first_dataset,"AE")
contract_date = excol_to_list(first_dataset,"AF")

doc_type = excol_to_list(first_dataset,"AG")
doc_number = excol_to_list(first_dataset,"AK")
doc_date = excol_to_list(first_dataset,"AL")

summ_without_nds = excol_to_list(first_dataset,"AM")
summ_nds = excol_to_list(first_dataset,"AO")
full_summ = excol_to_list(first_dataset,"AP")




def create_eschf_list():
	spisok_eschf = []
	for i in range(len(country_code)):
		eschf = {'country_code':country_code[i],'unp':str(provider_unp[i]),'contragent_name':provider_name[i],
		'numb':doc_number[i],'doc_type':doc_type[i], 'summ':full_summ[i], 
		'summ_without_nds':summ_without_nds[i], 'nds':summ_nds[i],'doc_date':str(doc_date[i])}
		spisok_eschf +=[eschf]
	return spisok_eschf 

#!!!!!!!!!!!!!!!!!!!https://ru.stackoverflow.com/questions/628315/%D0%9A%D0%B0%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%B4%D0%B8%D0%BD%D0%B8%D1%82%D1%8C-%D0%BD%D0%B5%D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B5%D0%B9/628329
#https://habrahabr.ru/post/85459/
#https://ru.stackoverflow.com/questions/427942/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-2-%D1%83%D1%85-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-python
#https://ru.stackoverflow.com/questions/427942/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-2-%D1%83%D1%85-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-python



a = get_docs_lists(cur,'2017-11-01','2017-11-30')
def create_tn_and_acts_list():
	vse=[]
	for i in a:
		vse =vse+i
	return vse


def create_podgot_base_list(in_list):
	out_list =[]
	for i in in_list:
		out_list +=[{'unp':i['unp'],'name':i['contragent_name'],'summ':i['summ']}]
	return out_list



in_base = create_tn_and_acts_list()
in_eschf = create_eschf_list()


podgot_base_list = create_podgot_base_list(in_base)
podgot_eshf_list = create_podgot_base_list(in_eschf)




def dif_list():
	spisok_edin = []
	not_in_base =[]
	not_in_portal = []

	for i in create_eschf_list():
		for k in range(len(create_tn_and_acts_list())):
			if create_tn_and_acts_list()[k]['summ'] == i['summ']:
				spisok_edin += [(i['contragent_name'],i['unp'],i['summ'],i['summ_without_nds'],i['nds'])]
	return spisok_edin




print(podgot_base_list)
print(podgot_eshf_list)

print(len(podgot_base_list))
print(len(podgot_eshf_list))

palg = [x for x in podgot_eshf_list + podgot_base_list if x not in podgot_eshf_list or x not in podgot_base_list]


alt = [i['summ'] for i in create_tn_and_acts_list() if i['summ'] not in create_eschf_list()]
bb = [i['summ'] for i in create_eschf_list() if i['summ'] not in create_tn_and_acts_list()]
print(len(bb))

>>> import itertools

>>> a = [{'a': '1'}, {'c': '2'}]
>>> b = [{'a': '1'}, {'b': '2'}]
>>> intersec = [item for item in a if item in b]
>>> sym_diff = [item for item in itertools.chain(a,b) if item not in intersec]

>>> intersec
[{'a': '1'}]
>>> sym_diff
[{'c': '2'}, {'b': '2'}

[{'unp': '691817469', 'summ': 49299.17, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '691817469', 'summ': 8.4, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '691817469', 'summ': 21007.74, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '691817469', 'summ': 73836.66, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '101272822', 'summ': 289.02, 'name': 'ОДО "Авангардспецмонтаж"'}, 
{'unp': '191800325', 'summ': 995.5, 'name': 'ООО "Огнеспас"'}, 
{'unp': '102302863', 'summ': 106.19, 'name': 'Минский филиал РУП "Белтелеком"'},
{'unp': '100071593', 'summ': 3310.36, 'name': 'РУП "Минскэнерго" филиад "Энергосбыт"'}, 
{'unp': '100071593', 'summ': 13.98, 'name': 'РУП "Минскэнерго" филиад "Энергосбыт"'}, 
{'unp': '100646299', 'summ': 260.64, 'name': 'ЗАО "ПРОМЭНЕРГОСТРОЙ"'}, 
{'unp': '100308563', 'summ': 714.63, 'name': 'УП "Мингаз"'}, 
{'unp': '100308563', 'summ': 45.06, 'name': 'УП "Мингаз"'},
{'unp': '691536883', 'summ': 35.68, 'name': 'Государственное предприятие Водоканал Минского района'}, 
{'unp': '800013732', 'summ': 106.0, 'name': 'СООО "Мобильные ТелеСистемы"'}, 
{'unp': '101120215', 'summ': 1.44, 'name': 'Минский филиал РУП  "Белпочта"'}, 
{'unp': '192514775', 'summ': 40.84, 'name':'ЧУП "Портал цен"'}, 
{'unp': '192287331', 'summ': 28.69, 'name': 'Торговое унитарное предприятие "Проект дилбай"'}, 
{'unp': '191118996', 'summ': 635.48, 'name': 'ИООО Газпромнефть Белнефтепродукт'},
{'unp': '391399801', 'summ': 319.9, 'name': 'ООО "Суперасуп"'}, 
{'unp': '600112981', 'summ': 1339.2,'name': 'ЧУП МАВ'}, 
{'unp': '191307958', 'summ': 105.6, 'name': 'СООО "Ремондис"'}, 
{'unp': '191307958', 'summ': 7.92, 'name': 'СООО "Ремондис"'}, 
{'unp': '191307958', 'summ': 105.6, 'name': 'СООО "Ремондис"'}, 
{'unp': '100162047', 'summ': 52.13, 'name': 'НП ОДО "Фармэкс"'}, 
{'unp': '391395821', 'summ': 222.0, 'name': 'ООО "Вольтра"'},
{'unp': '192743895', 'summ': 535.0, 'name': 'ООО "Аймаркет трейд"'},
{'unp': '690301556', 'summ': 208.83, 'name': 'ООО "Капитанарти"'},
{'unp': '190908204', 'summ': 264.0, 'name': 'ЧТУП "Комлайнсервис"'}]


[{'unp': '691817469.0', 'summ': 8.4, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '100646299.0', 'summ': 260.64, 'name': 'ЗАО "ПРОМЭНЕРГОСТРОЙ"'},
{'unp': '691817469.0', 'summ': 21007.74, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '691817469.0', 'summ': 49299.17, 'name': 'ООО "Авангардспецмонтажплюс"'}, 
{'unp': '100162047.0', 'summ': 52.13, 'name': 'НПОДО "ФАРМЭК"'}, 
{'unp': '391395821.0', 'summ': 222.0, 'name': 'Общество с ограниченнойответственностью "Вольтра"'}, 
{'unp': '600112981.0', 'summ': 1339.2, 'name': 'ЧУП "МАВ" РБ'}, 
{'unp': '192743895.0', 'summ': 535.0, 'name': 'Обществос ограниченной ответственностью "Аймаркет Трейд"'}, 
{'unp': '100071593.0', 'summ': -13.98, 'name': 'РУП"Минскэнерго" ф-л"Энергосбыт" г.Минск,РБ'}, 
{'unp': '102302863.0', 'summ': 106.19, 'name': 'МИНСКИЙ ФИЛИАЛ РУП "БЕЛТЕЛЕКОМ"'}, 
{'unp': '191118996.0', 'summ': 635.48, 'name': 'ИООО "Газпромнефть-Белнефтепродукт"'}, 
{'unp': '691536883.0', 'summ': 35.68, 'name': 'Государственное предприятие Водоканал Минского района'}, 
{'unp': '101120215.0', 'summ': 1.44, 'name': 'Минский филиал РУП Белпочта'}, 
{'unp': '192514775.0', 'summ': 40.84, 'name': 'Частное унитарное предприятие по оказанию услуг "Портал цен"'}, 
{'unp': '191800325.0', 'summ': 995.5, 'name': 'ООО "Огнеспас"'}, 
{'unp': '100308563.0', 'summ': -45.06, 'name': 'Производственное республиканское унитарное предприятие "МИНГАЗ"'}, 
{'unp': '100308563.0', 'summ': 714.63, 'name': 'Производственное республиканское унитарное предприятие "МИНГАЗ"'}, 
{'unp': '391399801.0', 'summ': 319.9, 'name': 'ООО "СуперАСуп", РБ'}, 
{'unp': '800013732.0', 'summ': 106.0, 'name': 'Совместное общество с ограниченной ответственностью "Мобильные ТелеСистемы"'}, 
{'unp': '190908204.0', 'summ': 264.0, 'name': 'ЧТУП "КомЛайнСервис"'}, 
{'unp': '191307958.0', 'summ': 105.6, 'name': 'Совместное общество с ограниченной ответственностью "РЕМОНДИС Минск"'}, 
{'unp': '191307958.0', 'summ': 7.92, 'name': 'Совместное общество с ограниченной ответственностью "РЕМОНДИС Минск"'}