#! /usr/bin/env python
# -*- coding: utf-8 -*
import dbf
from openpyxl import load_workbook,Workbook


excel_document = 'amedenta.xlsx'

amedenta_list = load_workbook(excel_document,data_only = True)

main_inner_sheet = amedenta_list.active


#names = (name, code, auantity, unit, price, summ, tnvd, weight, weight_summ, country)

def	get_excel_data():
	data_from_excel =[]

	for i in range(6,main_inner_sheet.max_row):
		if main_inner_sheet.cell(row=i, column=3).value != None:
			data_from_excel += [(
								str(main_inner_sheet.cell(row=i, column=3).value.decode('cp1251').encode('utf8')),
								str(main_inner_sheet.cell(row=i, column=4).value),
								str(main_inner_sheet.cell(row=i, column=5).value),
								main_inner_sheet.cell(row=i, column=6).value,
								str(main_inner_sheet.cell(row=i, column=7).value),
								str(main_inner_sheet.cell(row=i, column=8).value),
								str(main_inner_sheet.cell(row=i, column=9).value),
								str(main_inner_sheet.cell(row=i, column=10).value),
								str(round(main_inner_sheet.cell(row=i, column=11).value,3)),
								main_inner_sheet.cell(row=i, column=12).value,
								)]


	return data_from_excel
	pass

data = get_excel_data()
print(data[2])
table = dbf.Table('DH3091')

table.open()
"""
dbf.ver_33.Table('temptable.dbf')
for datum in((u'\xcf\xe0\xf1\xf2\xe0 Cleanic Mint, \xe1\xe5\xe7 \xf4\xf2\xee\xf0\xe0, 100 \xe3','3183', '5', '780', '3900', '33069000', '0.14', '0.7'),):
    table.append(datum)

"""