#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt


Excel = win32com.client.Dispatch("Excel.Application")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

first_list = Excel.Workbooks.Open(BASE_DIR+'ertex_in.xls')
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
	list_name = [r[0].value for r in dataset_name.Range(interval.format(col_name,col_name))]
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

	codes =[]
	prices =[]
	comings_to_stocs = []

	new_codes =[]
	new_prices =[]
	new_comings_to_stocs = []

	for i in list_length:
		if (list_of_cols[4][i] != 0.0 and list_of_cols[4][i] != None and list_of_cols[0][i] != None and list_of_cols[1][i] != None):
			warehouse_data_dict = {'номер':list_of_cols[1][0], '1C_код':list_of_cols[1][i], 'остаток на складе':list_of_cols[2][i],'сумма остатка':list_of_cols[3][i], 'приход на склад':list_of_cols[4][i],'цена': list_of_cols[5][i]}
			warehouse_update_list += [warehouse_data_dict]


	for i in warehouse_update_list:
		codes +=[i['1C_код']]
		prices +=[i['цена']]
		comings_to_stocs += [i['приход на склад']]	
	



		if i['остаток на складе'] != None:
			if i['остаток на складе']* i['цена'] != i['сумма остатка']:
				new_codes+=[i['1C_код']]
				new_prices +=[i['сумма остатка']/i['остаток на складе']]
				new_comings_to_stocs += [i['приход на склад']]		

		
	return (warehouse_update_list,codes,prices,comings_to_stocs,new_codes,new_prices,new_comings_to_stocs)
	pass




codes = get_warehouse_data()[1]
prices = get_warehouse_data()[2]
comings = get_warehouse_data()[3]

new_codes = get_warehouse_data()[4]
new_prices = get_warehouse_data()[5]
new_comings = get_warehouse_data()[6]

#записываем последовательность
def import_into_excel(document_name, *args):
	book = xlwt.Workbook('utf8')
	sheet = book.add_sheet('поступление на склад')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = Excel.Workbooks.Open(BASE_DIR+document_name)
	active_sheet = active_doc.ActiveSheet
	active_sheet.Cells(2,2).value ="test"

	a = 3
	active_sheet.Cells(2,1).value ="Код в 1С"
	for code in args[0]:
		active_sheet.Cells(a,1).value = code
		a = a + 1

	b = 3
	active_sheet.Cells(2,2).value ="Приход за месяц"
	for coming in args[1]:
		active_sheet.Cells(b,2).value = coming
		b = b + 1


	c = 3
	if args[2] == new_prices:
		active_sheet.Cells(2,3).value ="Новая цена"
	else: 
		active_sheet.Cells(2,3).value ="Цена за единицу"	
		pass
	for price in args[2]:
		active_sheet.Cells(c,3).value = price
		c = c + 1


	active_doc.Save()
	active_doc.Close()
	Excel.Quit()
	pass

#import_into_excel('ertex_out.xls',codes,comings,prices)
import_into_excel('ertex_out_new.xls',new_codes,new_comings,new_prices)


#сохраняем рабочую книгу