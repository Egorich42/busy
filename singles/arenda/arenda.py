#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys
path_to_file = os.path.dirname(os.path.abspath(__file__))+'\\'
convert_to_list = path_to_file.split('\\')[:-2]
root_path = '\\'.join(convert_to_list)
sys.path.append(root_path)
import base




BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

first_list = base.Excel.Workbooks.Open(BASE_DIR+'transkom_in.xls')
first_dataset = first_list.ActiveSheet


company_list = ('united', 'mitada','bona_kauza')
names_cells = [r[0].value for r in first_dataset.Range("B2:B14")]
price_cells = [r[0].value for r in first_dataset.Range("C2:C14")]

def create_first_arenda_list():
	list_length = list(range(len(names_cells))) 
	arenda_list=[]
	list_of_lists = (names_cells, price_cells)
	for i in list_length:
		arenda_dict = {'name':list_of_lists[0][i], 'price':list_of_lists[1][i]}
		arenda_list += [arenda_dict]
		pass
	return arenda_list
	pass




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



#записываем последовательность
def import_into_excel(document_name, names, arenda):
	book = base.xlwt.Workbook('utf8')
	sheet = book.add_sheet('аренда')

	sheet.portrait = False

	sheet.set_print_scaling(85)
	created_book = book.save(document_name)
	active_doc = base.Excel.Workbooks.Open(BASE_DIR+document_name)
	active_sheet = active_doc.ActiveSheet

	i = 30
	for rec in names:
		active_sheet.Cells(i,2).value = rec
		i = i + 1

	m = 30
	for sec in arenda:
		active_sheet.Cells(m,3).value = sec
		m = m + 1


	active_doc.Save()
	active_doc.Close()
	base.Excel.Quit()
	pass

import_into_excel('bonanaa!!!.xls',names_list, arenda[2])
import_into_excel('mitadamnd.xls',names_list, arenda[1])
import_into_excel('bonamnt.xls',names_list, arenda[0])



#сохраняем рабочую книгу
