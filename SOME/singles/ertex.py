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

interval.format("B","B")
interval.format("f","f")
interval.format("H","H")
interval.format("I","I")
interval.format("J","J")
interval.format("K","K")

numbers = [r[0].value for r in first_dataset.Range(interval.format("B","B"))]
odinc_code = [r[0].value for r in first_dataset.Range(interval.format("f","f"))]
remains_on_warehouse = [r[0].value for r in first_dataset.Range(interval.format("H","H"))]
remains_summ= [r[0].value for r in first_dataset.Range(interval.format("I","I"))]
coming_to_warehouse = [r[0].value for r in first_dataset.Range(interval.format("J","J"))]
price = [r[0].value for r in first_dataset.Range(interval.format("K","K"))]

list_of_cols = (odinc_code,remains_on_warehouse,remains_summ,coming_to_warehouse,price)

def get_warehouse_data():
	list_length = list(range(len(odinc_code))) 
	warehouse_update_list=[]
	for i in list_length:
		if (list_of_cols[3][i] != 0.0 and list_of_cols[3][i] != None and list_of_cols[0][i] != None):
			warehouse_data_dict = {'1C_код':list_of_cols[0][i], 'остаток на складе':list_of_cols[1][i],'сумма остатка':list_of_cols[2][i], 'приход на склад':list_of_cols[3][i],'цена': list_of_cols[4][i]}
			warehouse_update_list += [warehouse_data_dict]
		pass
	return warehouse_update_list
	pass

get_warehouse_data()
print(len(get_warehouse_data()))

"""


def create_all_lists():
	rent_parameters = create_first_arenda_list()
	rent_list=[]
	mnojitel = [0.1984, 0.1522, 0.1111]
	for m in mnojitel:
		arendator_price = [round(i['price']*m, 2) for i in rent_parameters if type(i['price'])==float]

		sum_price = round(sum(arendator_price),2)

		rent_list +=[([i for i in arendator_price],(sum_price))]

	return rent_list
	pass


names_list = [i['name'] for i in create_first_arenda_list()]
arenda = [create_all_lists()[i][0] for i in (0,1,2)]



#http://www.py-my.ru/post/4e15588e1d41c81105000003

first_list = Excel.Workbooks.Open(BASE_DIR+'transkom_in.xls')
first_dataset = first_list.ActiveSheet


#записываем последовательность
def import_into_excel(document_name, names, arenda):
	book = xlwt.Workbook('utf8')
	sheet = book.add_sheet('аренда')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = Excel.Workbooks.Open(BASE_DIR+document_name)
	active_sheet = active_doc.ActiveSheet

	i = 3
	for rec in names:
		active_sheet.Cells(i,2).value = rec
		i = i + 1

	m = 30
	for sec in arenda:
		active_sheet.Cells(m,3).value = sec
		m = m + 1


	active_doc.Save()
	active_doc.Close()
	Excel.Quit()
	pass

import_into_excel('ertex_out.xls',names_list, arenda[2])


"""

#сохраняем рабочую книгу