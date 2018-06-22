import sqlite3

import os
import openpyxl
from openpyxl import load_workbook,Workbook
from forge import create_list_of_table_values, grouping_by_key
from forge import sel_out_pays_br, sel_out_docs_br, sel_out_docs_br_back, sel_income_docs_br, sel_income_pays_br, sel_income_pays_br_dpd, sel_income_pays_br_back 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'



class Hvosty:
	def __init__(self, base_name=None, start_data = None, end_data = None, contragent_id = None):
		self.base_name = base_name
		self.start_data = start_data
		self.end_data = end_data
		self.contragent_id = contragent_id

	def get_ops_list(self):
		conn = sqlite3.connect(self.base_name )
		cur = conn.cursor()
		#####################
		income_pays_list = create_list_of_table_values(cur.execute(sel_income_pays_br_sv_act.format(self.contragent_id, self.start_data, self.end_data)),cur.description)
		income_pays_list_dpd = create_list_of_table_values(cur.execute(sel_income_pays_br_dpd_sv_act.format(self.start_data, self.end_data)),cur.description)
		income_pays_list_pay_back = create_list_of_table_values(cur.execute(sel_income_pays_br_back_sv_act.format(self.start_data, self.end_data)),cur.description)
		#####################


		income_docs = create_list_of_table_values(cur.execute(sel_income_docs_br_sv_act.format(self.contragent_id, self.start_data, self.end_data)),cur.description)
		#####################


		out_docs = create_list_of_table_values(cur.execute(sel_out_docs_br_sv_act.format(self.contragent_id, self.start_data, self.end_data)),cur.description)
		# а вот это что такое? out_docs_back = create_list_of_table_values(cur.execute(sel_out_docs_br_back_sv_act.format(self.contragent_id, self.start_data, self.end_data)),cur.description)
		#####################


		out_pays = create_list_of_table_values(cur.execute(sel_out_pays_br_sv_act.format(self.contragent_id, self.start_data, self.end_data)),cur.description)


		conn.commit()
		conn.close()
		return income_pays_list+out_docs, income_pays_list_dpd+income_pays_list_pay_back+income_docs
		pass

	def contragent_ops_result(self, income_list):
		result = []
		for contragent in income_list:
			result +=[{'name': contragent[0]['contragent_name'], 'parent':contragent[0]['parent'],  'sum':round(sum([float(x['summ']) for x in contragent]),2)}]
		return result
		pass
		

	def show_contragent_balance(self):
#		provider_debt = []#предоплатили поставщику, не отгрузил
#		provider_prepay = []#поставил, не оплатили еще

#		buyer_debt = []#покупатель должен денег
#		buyer_prepay = []#покупатель предоплатил, не отгрузили

		out_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[2],'parent'))
		income_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[3], 'parent'))

		income_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[0], 'parent'))
		outcome_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[1], 'parent'))

		provider_debt = self.found_result(out_pays, income_docs)[0]
		provider_prepay = self.found_result(out_pays, income_docs)[1]

		buyer_debt =self.found_result(income_pays, outcome_docs)[0]
		buyer_prepay = self.found_result(income_pays, outcome_docs)[1]

		return provider_debt, provider_prepay, buyer_debt, buyer_prepay
		pass



balance_lists = Hvosty("avangard.sqlite","'"+ '2017-01-01'+"'", "'"+'2018-03-30'+"'","'60'").get_ops_list()

"""
Бусы -6J
ИВ и компания -V
ЖКУ ОАО "МАПИД" - 60

Дилогос и Теплосервис - уже фсьо
"""