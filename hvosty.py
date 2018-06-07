import sqlite3


from TESTO import create_list_of_table_values, grouping_by_key
from TESTO import sel_out_pays_br, sel_out_docs_br, sel_out_docs_br_back, sel_income_docs_br, sel_income_pays_br, sel_income_pays_br_dpd, sel_income_pays_br_back 



class Hvosty:
	def __init__(self, base_name=None, start_data = None, end_data = None):
		self.base_name = base_name
		self.start_data = start_data
		self.end_data = end_data

	def get_ops_list(self):
		conn = sqlite3.connect(self.base_name )
		cur = conn.cursor()

		out_pays_list = create_list_of_table_values(cur.execute(sel_out_pays_br.format(self.start_data, self.end_data)),cur.description)
		income_docs_list = create_list_of_table_values(cur.execute(sel_income_docs_br.format(self.start_data, self.end_data)),cur.description)

		income_pays_list = create_list_of_table_values(cur.execute(sel_income_pays_br.format(self.start_data, self.end_data)),cur.description)
		out_docs_list = create_list_of_table_values(cur.execute(sel_out_docs_br.format(self.start_data, self.end_data)),cur.description)

		conn.commit()
		conn.close()
		return (out_pays_list, income_docs_list, income_pays_list, out_docs_list)
		pass


	def contragent_ops_result(self, income_list):
		result = []
		for contragent in income_list:
			result +=[{'name': contragent[0]['contragent_name'], 'parent':contragent[0]['parent'],  'sum':round(sum([float(x['summ']) for x in contragent]),2)}]
		return result
		pass
		


	def found_result(self, one_list, sec_list):
		out_list = []
		in_list = []
		for doc in one_list:
			for ops in sec_list:
				if doc['parent'] == ops['parent']:
					if doc['sum'] > ops['sum']:
						out_list+=[{'name':doc['name'], 'summ':round(doc['sum'] -  ops['sum'],2)}]

					if doc['sum'] < ops['sum']:
						in_list+=[{'name':doc['name'], 'summ': round(ops['sum'] - doc['sum'],2)}]

		return(out_list, in_list)			
		pass


	def show_contragent_balance(self):
#		provider_debt = []#предоплатили поставщику, не отгрузил
#		provider_prepay = []#поставил, не оплатили еще

#		buyer_debt = []#покупатель должен денег
#		buyer_prepay = []#покупатель предоплатил, не отгрузили

		out_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[0],'parent'))
		income_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[1], 'parent'))

		income_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[2], 'parent'))
		outcome_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[3], 'parent'))



		provider_debt = self.found_result(out_pays, income_docs)[0]
		provider_prepay = self.found_result(out_pays, income_docs)[1]

		buyer_debt =self.found_result(income_pays, outcome_docs)[0]
		buyer_prepay = self.found_result(income_pays, outcome_docs)[1]

		return (provider_debt, provider_prepay, buyer_prepay, buyer_debt)
		pass

print(Hvosty("avangard.sqlite","'"+ '2016-01-30'+"'", "'"+'2018-06-01'+"'").show_contragent_balance())

