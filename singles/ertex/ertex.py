#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

base_list = BASE_DIR+'transkom_in.xlsx'
wb = load_workbook(base_list)
sheet = wb.active


def	get_cols_data(col_name,multiplier,sheetname):
		codes_1c = []
		remains_on_warehouse=[]
		remains_summ=[]
		income_summ=[]
		past_price=[]

		new_prices=[]

		main_sheet = wb["jan"]
		for i in range(6,main_sheet.max_row):
			if main_sheet.cell(row=i, column=5).value != None:
				codes_1c +=[main_sheet.cell(row=i, column=5).value]
				remains_on_warehouse+=[main_sheet.cell(row=i, column=8).value]
				remains_summ+=[main_sheet.cell(row=i, column=9).value]
				income_summ+=[main_sheet.cell(row=i, column=10).value]
				past_price +=[main_sheet.cell(row=i, column=11).value]

		for i in range(len(codes_1c)):
			if remains_on_warehouse[i]/remains_summ[i] != past_price[i]:
				new_prices +=[round(remains_on_warehouse[i]/remains_summ[i],2)]

						pass		






united_data = get_cols_data(3,0.1984,"United")
mitada_data = get_cols_data(3,0.1522,"Mitada")
bona_data = get_cols_data(3,0.1111,"Bona")
