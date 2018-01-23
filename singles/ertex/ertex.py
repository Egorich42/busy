#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys
path_to_file = os.path.dirname(os.path.abspath(__file__))+'\\'
convert_to_list = path_to_file.split('\\')[:-2]
root_path = '\\'.join(convert_to_list)
sys.path.append(root_path)
import base


first_list = base.Excel.Workbooks.Open(base.BASE_DIR+'ertex_in_nov.xls')
first_dataset = first_list.ActiveSheet



start_point = base.find_first_point(first_dataset)
endpoint = base.find_endpoint(first_dataset,start_point,'ИТОГО:')
interval = "{}"+str(start_point)+":"+"{}"+str(endpoint)



numbers = base.excol_to_list(first_dataset,"B",interval)
odinc_code= base.excol_to_list(first_dataset,"F",interval)
remains_on_warehouse= base.excol_to_list(first_dataset,"H",interval)
remains_summ= base.excol_to_list(first_dataset,"I",interval)
coming_to_warehouse= base.excol_to_list(first_dataset,"J",interval)
price= base.excol_to_list(first_dataset,"K",interval)





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

transformed_warehouse_data = base.np.array(get_warehouse_data())



#записываем последовательность
def import_into_excel(document_name, number):

	codes_1c = [x['1C_код'] for x in transformed_warehouse_data[number]]
	counts =[x['приход на склад'] for x in transformed_warehouse_data[number]]
	prices =[x['цена'] for x in transformed_warehouse_data[number]]


	book = base.xlwt.Workbook('utf8')
	sheet = book.add_sheet('поступление на склад')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = base.Excel.Workbooks.Open(base.BASE_DIR+document_name)
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
	base.Excel.Quit()
	pass

#import_into_excel('ertex_out.xls',1)
import_into_excel('ertex_out_new.xls',0)