#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys
path_to_file = os.path.dirname(os.path.abspath(__file__))+'\\'
convert_to_list = path_to_file.split('\\')[:-2]
root_path = '\\'.join(convert_to_list)
sys.path.append(root_path)
import sql_commands as sq_c
from dbfread import DBF

import sqlite3


from openpyxl import load_workbook,Workbook
import itertools
from itertools import groupby
from operator import itemgetter


dbf_esch='D:\DATA_SETS\himprom_den\SC37543.DBF'
dbf_contragents='D:\DATA_SETS\himprom_den\SC167.DBF'


def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass

esch_list_dbf = get_data_from_dbf(dbf_esch)
contragents_list_dbf = get_data_from_dbf(dbf_contragents)

def get_data_eschf():
	values_list = []
	for i in esch_list_dbf:	
		values_list += [(
						dict(i)['DESCR'].encode('latin1').decode('cp1251'), 
						dict(i)['PARENTEXT'].replace(" ", ""), 
						dict(i)['SP37497'], 
						dict(i)['SP37498'],
						dict(i)['ISMARK'],
						)]
	return values_list	
	pass


def get_data_contragents():
	values_list = []
	for i in contragents_list_dbf:	
		values_list += [(
					dict(i)['ID'].replace(" ", ""), 
					dict(i)['SP137'],
					dict(i)['DESCR'].encode('latin1').decode('cp1251'), 
					dict(i)['SP134'].encode('latin1').decode('cp1251'), 
					dict(i)['ISMARK'],
					)]
	return values_list				
	pass

contragents = get_data_contragents()
eschf_list = get_data_eschf()


"""
conn = sqlite3.connect('hpo.sqlite')
c = conn.cursor()
c.execute("CREATE table IF NOT EXISTS contragents (id,unp,contragent_name,full_name, deleted);")
c.execute("CREATE table IF NOT EXISTS outer_eschf (document_name,contragent,full_sum, nds, deleted);")


c.executemany('INSERT INTO contragents VALUES (?,?,?,?,?)', contragents)
c.executemany('INSERT INTO outer_eschf VALUES (?,?,?,?,?)', eschf_list)


conn.commit()
conn.close()
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
portal_doc = BASE_DIR+'jan_out.xlsx'
portal_list = load_workbook(portal_doc,data_only = True)
main_inner_sheet = portal_list["jan"]


def	get_eschf_excel():
	first_list_from_excel =[]


	for i in range(4,main_inner_sheet.max_row):
		if  main_inner_sheet.cell(row=i, column=18) != "Аннулирован":
			first_list_from_excel += [{ "unp" : main_inner_sheet.cell(row=i, column=9).value, 
					"contragent_name" : main_inner_sheet.cell(row=i, column=11).value,
					"nds" : main_inner_sheet.cell(row=i, column=42).value,
					"full_sum" : main_inner_sheet.cell(row=i, column=43).value,
					}]

	return first_list_from_excel
	pass

#####################################################################################################################
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


docs_from_base = get_docs_lists(cur,'2017-11-01','2017-11-30')

def create_base_dicts_list(incoming_list):
	outcoming_list = []
	for i in incoming_list:
		outcoming_list+=[{'contragent_name': i[0]['contragent_name'], 'unp':i[0]['unp'], 'summ':round(sum([x['summ'] for x in i]),2)}]
	return outcoming_list
	pass


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



	