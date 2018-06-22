import sqlite3

import os
import openpyxl
from openpyxl import load_workbook,Workbook
from forge import create_list_of_table_values, grouping_by_key

from forge import sel_income_pays_contragent, sel_out_docs_contragent, sel_income_docs_contragent, sel_out_docs_back_contragent, sel_income_pays_dpd_contragent, sel_income_pays_back_contragent, sel_out_pays_contragent

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
		income_pays_list = create_list_of_table_values(cur.execute(sel_income_pays_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)
		income_docs = create_list_of_table_values(cur.execute(sel_income_docs_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)



		income_pays_dpd = create_list_of_table_values(cur.execute(sel_income_pays_dpd_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)
		out_docs_list = create_list_of_table_values(cur.execute(sel_out_docs_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)
#		out_docs_list_back = create_list_of_table_values(cur.execute(sel_out_docs_back_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)



		income_pays_back = create_list_of_table_values(cur.execute(sel_income_pays_back_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)
		out_pays = create_list_of_table_values(cur.execute(sel_out_pays_contragent.format(self.start_data, self.end_data, self.contragent_id, )),cur.description)



		conn.commit()
		conn.close()
		return (income_pays_list+income_docs, out_docs_list+income_pays_dpd+out_pays)
		pass


	def contragent_ops_result(self, income_list):
		result = []
		for contragent in income_list:
			result +=[  {'document':contragent['document_name'], 'summ': contragent['summ'], 'dos_date':contragent['doc_date']}  ]
		suma = sum([float(x['summ']) for x in result])	
		return (result,suma)
		pass


	def robo(self):
		income = self.contragent_ops_result(self.get_ops_list()[0])
		outcome = self.contragent_ops_result(self.get_ops_list()[1])

		return income,outcome
		pass		


balance_lists = Hvosty("avangard.sqlite","'"+ '2018-01-01'+"'", "'"+'2018-06-13'+"'","'5'").robo()

print(balance_lists)