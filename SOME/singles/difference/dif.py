#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt

import sqlite3

import sql_commands as sq_c
import variables as var


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
		eschf = {'country_code':country_code[i],'unp':int(provider_unp[i]),'contragent_name':provider_name[i],
		'numb':doc_number[i],'doc_type':doc_type[i], 'summ':full_summ[i], 
		'summ_without_nds':summ_without_nds[i], 'nds':summ_nds[i],'doc_date':str(doc_date[i])}
		spisok_eschf +=[eschf]
	return spisok_eschf 



a = get_docs_lists(cur,'2017-11-01','2017-11-30')

#!!!!!!!!!!!!!!!!!!!https://ru.stackoverflow.com/questions/628315/%D0%9A%D0%B0%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%B4%D0%B8%D0%BD%D0%B8%D1%82%D1%8C-%D0%BD%D0%B5%D1%81%D0%BA%D0%BE%D0%BB%D1%8C%D0%BA%D0%BE-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D0%B5%D0%B9/628329
#https://habrahabr.ru/post/85459/
#https://ru.stackoverflow.com/questions/427942/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-2-%D1%83%D1%85-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-python
#https://ru.stackoverflow.com/questions/427942/%D0%A1%D1%80%D0%B0%D0%B2%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5-2-%D1%83%D1%85-%D1%81%D0%BF%D0%B8%D1%81%D0%BA%D0%BE%D0%B2-%D0%B2-python

def create_tn_and_acts_list():
	vse=[]
	for i in a:
		vse =vse+i
	return vse



def dif_list():
	spisok_edin = []
	not_in_base =[]
	not_in_portal = []

	for i in create_eschf_list():
		for k in range(len(create_tn_and_acts_list())):
			if create_tn_and_acts_list()[k]['summ'] == i['summ']:
				spisok_edin += ((i['contragent_name'],i['unp'],i['summ'],i['summ_without_nds'],i['nds']))
	return spisok_edin

dif_list()

print(type(create_tn_and_acts_list()))
print(type(dif_list()))


Res = [x for x in dif_list() if x in create_tn_and_acts_list()]
print(Res)