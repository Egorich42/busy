#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt
import sqlite3

import sql_commands as sq_c
import variables as var
import itertools    

import itertools
from operator import itemgetter
from itertools import groupby


conn = sqlite3.connect('hpo.sqlite')
cur = conn.cursor()

Excel = win32com.client.Dispatch("Excel.Application")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

first_list = Excel.Workbooks.Open(BASE_DIR+'hpo_in.xls')
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
		eschf = {'unp':str(int(provider_unp[i])),'contragent_name':provider_name[i],
		'numb':doc_number[i],'doc_type':doc_type[i], 'summ':full_summ[i], 
		'summ_without_nds':summ_without_nds[i], 'nds':summ_nds[i],'doc_date':str(doc_date[i])}
		spisok_eschf +=[eschf]
	return spisok_eschf 


docs_from_base = get_docs_lists(cur,'2017-11-01','2017-11-30')

def create_base_dicts_list(incoming_list):
	outcoming_list = []
	for i in incoming_list:
		outcoming_list+=[{'contragent_name': i[0]['contragent_name'], 'unp':i[0]['unp'], 'summ':round(sum([x['summ'] for x in i]),2)}]
	return outcoming_list
	pass




def create_eschf_dict_list():
	sorted_eschf = sorted(create_eschf_list(), key=itemgetter('unp'))
	full = []
	for key, group in itertools.groupby(sorted_eschf, key=lambda x:x['unp']):
		art = list(group)
		full+=[art]
	return create_base_dicts_list(full)

base_list = create_base_dicts_list(docs_from_base)
eschf_list = create_eschf_dict_list()



def not_in_base():
	paskuda = create_eschf_dict_list()
	for i in create_base_dicts_list(docs_from_base):
		for k in range(len(create_eschf_dict_list())):
			if create_eschf_dict_list()[k]['summ'] == i['summ'] and create_eschf_dict_list()[k]['unp'] == i['unp']:
				paskuda.remove(create_eschf_dict_list()[k])
	return paskuda


def not_in_portal():
	paskuda = create_base_dicts_list(docs_from_base)
	for i in create_eschf_dict_list():
		for k in range(len(create_base_dicts_list(docs_from_base))):
			if create_base_dicts_list(docs_from_base)[k]['summ'] == i['summ'] and create_base_dicts_list(docs_from_base)[k]['unp'] == i['unp']:
				paskuda.remove(create_base_dicts_list(docs_from_base)[k])
	return paskuda



def not_in_suka():
	paskuda = not_in_base()
	cortney = not_in_portal()
	net_v_baze = []
	net_na_port = []
	
	for i in not_in_portal():
		for k in not_in_base():
			if k['unp'] == i['unp'] and i['summ'] > k['summ']:
				net_na_port += [{'contragent_name':i['contragent_name'],'unp':i['unp'], 'summ': round(i['summ'] - k['summ'], 3)}]
				
			if k['unp'] == i['unp'] and i['summ'] < k['summ']:
				net_v_baze += [{'contragent_name':i['contragent_name'],'unp':i['unp'], 'summ': round(k['summ'] - i['summ'], 3)}]	
				
			if k['unp'] == i['unp']:
				paskuda.remove(k)#not in base
				cortney.remove(i)#not in eschf
		

	return (net_na_port+net_v_baze,paskuda+cortney)



def final_list(listik):
	names = [i['contragent_name'] for i in listik]
	unps = [i['unp'] for i in listik]
	sums = [i['summ'] for i in listik]
	ndses = [round(i['summ']/6, 2) for i in listik]
	return (names,unps,sums,ndses)


col_names = ("Контрагент","УНП","Полная сумма","НДС")


def import_into_excel(document_name, inner_list):
	book = xlwt.Workbook('utf8')
	sheet = book.add_sheet('разница')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = Excel.Workbooks.Open(BASE_DIR+document_name)
	active_sheet = active_doc.ActiveSheet	

	a = 3
	for i in range(len(inner_list)):
		active_sheet.Cells(2,i+1).value = col_names[i]
		for code in inner_list[i]:
			active_sheet.Cells(a,i+1).value = code
			a = a + 1

	active_doc.Save()
	active_doc.Close()
	Excel.Quit()
	pass

import_into_excel('himpro_out_base.xls',final_list(not_in_suka()[0]))	
import_into_excel('himpro_out_portal.xls',final_list(not_in_suka()[1]))	
