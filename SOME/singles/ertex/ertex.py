#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt
import numpy as np

Excel = win32com.client.Dispatch("Excel.Application")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

first_list = Excel.Workbooks.Open(BASE_DIR+'ertex_in_nov.xls')
first_dataset = first_list.ActiveSheet


def find_first_point(dataset):
	for i in range(1,10):
		if dataset.Cells(i,3).value != None and dataset.Cells(i,2).value == 1.0:
			dataset.Cells(i,2).value
			return i
			pass

def find_endpoint(dataset,start):
	for i in range(start,510):
		if dataset.Cells(i,5).value =='ИТОГО:':
			return i-1
			pass


start_point = find_first_point(first_dataset)
endpoint = find_endpoint(first_dataset,start_point)
interval = "{}"+str(start_point)+":"+"{}"+str(endpoint)


def excol_to_list(dataset_name, col_name):
	list_name = np.array([r[0].value for r in dataset_name.Range(interval.format(col_name,col_name))])
	return list_name
	pass


numbers = excol_to_list(first_dataset,"B")
odinc_code= excol_to_list(first_dataset,"F")
remains_on_warehouse= excol_to_list(first_dataset,"H")
remains_summ= excol_to_list(first_dataset,"I")
coming_to_warehouse= excol_to_list(first_dataset,"J")
price= excol_to_list(first_dataset,"K")


list_of_cols = (numbers,odinc_code,remains_on_warehouse,remains_summ,coming_to_warehouse,price)


def get_warehouse_data():
	list_length = list(range(len(numbers))) 

	warehouse_update_list=[]
	no_change =[]
	change_price = []
	new_items_on_warehouse = []
	old_prices =[]


	for i in list_length:
		if (list_of_cols[4][i] != 0.0 and list_of_cols[4][i] != None and list_of_cols[0][i] != None):
			warehouse_data_dict = { '1C_код':list_of_cols[1][i], 'остаток на складе':list_of_cols[2][i],'сумма остатка':list_of_cols[3][i], 'приход на склад':list_of_cols[4][i],'цена': list_of_cols[5][i]}
			warehouse_update_list += [warehouse_data_dict]

			
	for i in warehouse_update_list:
		if i['остаток на складе'] != None:
			if i['цена']*i['остаток на складе'] == i['сумма остатка']:
				no_change +=[i]	

			else:
				change_price +=[i]
				old_prices +=[i['сумма остатка']/i['остаток на складе']]
		if	i['остаток на складе'] == None:
			new_items_on_warehouse +=[i]	


	
	return (change_price,no_change+new_items_on_warehouse)
	pass

transformed_warehouse_data = np.array(get_warehouse_data())



#записываем последовательность
def import_into_excel(document_name, number):

	codes_1c = [x['1C_код'] for x in transformed_warehouse_data[number]]
	counts =[x['приход на склад'] for x in transformed_warehouse_data[number]]
	prices =[x['цена'] for x in transformed_warehouse_data[number]]


	book = xlwt.Workbook('utf8')
	sheet = book.add_sheet('поступление на склад')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = Excel.Workbooks.Open(BASE_DIR+document_name)
	active_sheet = active_doc.ActiveSheet


	a = 3
	active_sheet.Cells(2,1).value ="Код в 1С"
	for code in codes_1c:
		active_sheet.Cells(a,1).value = code
		a = a + 1

	b = 3
	active_sheet.Cells(2,2).value ="Приход за месяц"
	for count in counts:
		active_sheet.Cells(b,2).value = count
		b = b + 1


	c = 3
	active_sheet.Cells(2,3).value ="цена"
	for price in prices:
		active_sheet.Cells(c,3).value = price
		c = c + 1


	active_doc.Save()
	active_doc.Close()
	Excel.Quit()
	pass

#import_into_excel('ertex_out.xls',1)
import_into_excel('ertex_out_new.xls',0)