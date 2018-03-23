#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys
import sqlite3
from openpyxl import load_workbook,Workbook
import itertools
from itertools import groupby
from operator import itemgetter
path_to_file = os.path.dirname(os.path.abspath(__file__))+'\\'
convert_to_list = path_to_file.split('\\')[:-2]
root_path = '\\'.join(convert_to_list)
sys.path.append(root_path)
import sql_commands as sq_c
import variables as var



BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
sql_base_name = 'pol.sqlite'
conn = sqlite3.connect(sql_base_name )
cur = conn.cursor()


excel_income = 'pol_in_oct_dec.xlsx'
excel_outcome = 'result.xlsx'

excel_sheet_name = "oct_dec"
output_sheet_name = "result"

data_start = "2017-10-01"
data_end=  "2017-12-31"


portal_doc = BASE_DIR+excel_income
portal_list = load_workbook(portal_doc,data_only = True)
main_inner_sheet = portal_list[excel_sheet_name]


output_doc = BASE_DIR+excel_outcome
output_list = load_workbook(output_doc,data_only = True)
main_out_sheet = output_list[output_sheet_name]


def sum_of_list(sum_name,income_list):
	return sum([x[sum_name] for x in income_list])
	pass


def	get_eschf_data():
	first_list_from_excel =[]
	full_grouped_list = []
	outcoming_list =[]

	for i in range(4,main_inner_sheet.max_row):
		if  main_inner_sheet.cell(row=i, column=18) != "Аннулирован" and main_inner_sheet.cell(row=i, column=2).value != None: 
			first_list_from_excel += [{ 
					"unp" : main_inner_sheet.cell(row=i, column=2).value, 
					"contragent_name" : main_inner_sheet.cell(row=i, column=4).value,
					"nds" : main_inner_sheet.cell(row=i, column=41).value,
					"full_sum" : main_inner_sheet.cell(row=i, column=42).value,
					}]

	sorted_list_from_excel = sorted(first_list_from_excel, key=itemgetter('unp'))

	for key, group in itertools.groupby(sorted_list_from_excel, key=lambda x:x['unp']):
		grouped_list_of_lists = list(group)
		full_grouped_list+=[grouped_list_of_lists]								


	for i in full_grouped_list:
		outcoming_list+=[{'name': i[0]['contragent_name'],'unp':str(i[0]['unp']), 'nds':round(sum([x['nds'] for x in i]),2)}]

	return outcoming_list
	pass


def transform_sql_to_list(cursor, request_command, *condition):
    if len(condition) ==2:
        sql_request = request_command.format(condition[0],condition[1])
    if len(condition) ==3:
        sql_request = request_command.format(condition[0],condition[1],condition[2])
    if len(condition) ==4:
        sql_request = request_command.format(condition[0],condition[1],condition[2],condition[3])

    return var.create_list_of_table_values(cursor.execute(sql_request),cursor.description)
    pass


def curent_finace_states(start, end, cursor):
	full_grouped_list = []
	outcoming_list = []

	list_vhod_nds_usl = transform_sql_to_list(cursor, sq_c.sel_vhod_usl_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
	list_vhod_nds_tn = transform_sql_to_list(cursor, sq_c.sel_vhod_tn_with_nds, sq_c.tn_buyers,  "'"+start+"'",  "'"+str(end)+"'" )
	list_tovary_nds  = transform_sql_to_list(cursor, sq_c.sel_tovary_with_vhod_nds,   "'"+start+"'",  "'"+str(end)+"'" )

	unsorted_full_list = [i for i in list_tovary_nds+list_vhod_nds_tn+list_vhod_nds_usl if i['nds'] != 0.0 and i['nds']!=None]

	sorted_list_from_base = sorted(unsorted_full_list, key=itemgetter('name'))


	for key, group in itertools.groupby(sorted_list_from_base, key=lambda x:x['name']):
		grouped_list_of_lists = list(group)
		full_grouped_list += [grouped_list_of_lists]								
							

	for i in full_grouped_list:
		outcoming_list+=[{'name': i[0]['name'],'unp':i[0]['unp'], 'nds':round(sum([x['nds'] for x in i]),2)}]

	return outcoming_list
	pass


def find_difference():
	not_in_excel = get_eschf_data()
	not_in_base = curent_finace_states(data_start, data_end, cur)

	for i in curent_finace_states(data_start, data_end, cur):
		for x in get_eschf_data():
			if i['unp'] == x['unp'] and i['nds'] == x['nds']:
				not_in_excel.remove(x)
				not_in_base.remove(i)

	for y in not_in_base:
		for n in not_in_excel:
			if n['unp'] == y['unp']:
				if n['nds'] > y['nds']:
					n['nds'] = n['nds'] - y['nds']
					not_in_base.remove(y)

				if n['nds'] < y['nds']:
					y['nds'] = y['nds'] - n['nds']
					not_in_excel.remove(n)
					[x for x in not_in_excel]

	return(not_in_excel,not_in_base)
	pass



def insert_into_excel():

	def insert_cell(row_val, col_val, cell_value):
		main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
		pass

	insert_cell(2, 1, "Контрагент")
	insert_cell(2, 4,"Контрагент")

	insert_cell(2, 2, "НДС")
	insert_cell(2, 5,"НДС")

	insert_cell(len(find_difference()[0])+4, 1,"Всего")
	insert_cell(len(find_difference()[1])+4, 4,"Всего")

	insert_cell(len(find_difference()[0])+4, 2,sum_of_list('nds', find_difference()[0]))
	insert_cell(len(find_difference()[1])+4, 5,	sum_of_list('nds', find_difference()[1]))


	for i in range(len(find_difference()[0])):
		insert_cell(i+3, 1, find_difference()[0][i]['name'])
		insert_cell(i+3, 2, find_difference()[0][i]['nds'])

	for i in range(len(find_difference()[1])):

		insert_cell(i+3, 4, find_difference()[1][i]['name'])
		insert_cell(i+3, 5, find_difference()[1][i]['nds'])

	output_list.save(filename = output_doc)
	pass


insert_into_excel()
