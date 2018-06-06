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


	def contragent_ops_result(self, income_list, sum_type):
		result = []
		for contragent in income_list:
			result +=[{'name': contragent[0]['contragent_name'], 'parent':contragent[0]['parent'],  sum_type:round(sum([float(x['summ']) for x in contragent]),2)}]
		return result
		pass
		

	def show_contragent_balance(self):

		out_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[0],'parent'), 'out_pays')
		income_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[1], 'parent'),'income_docs')

		income_pays = self.contragent_ops_result(grouping_by_key(self.get_ops_list()[2], 'parent'),'income_pays')
		outcome_docs= self.contragent_ops_result(grouping_by_key(self.get_ops_list()[3], 'parent'),'outcome_docs')


		providers_state = grouping_by_key(out_pays+income_docs,'parent')

		buyers_state = grouping_by_key(income_pays+outcome_docs,'parent')

		provider_debt = []#предоплатили поставщику, не отгрузил
		provider_prepay = []#поставил, не оплатили еще


		buyer_debt = []#покупатель должен денег
		buyer_prepay = []#покупатель предоплатил, не отгрузили

		for provider_state in providers_state:
			if len(provider_state)>1:
				for i in provider_state:
					if provider_state[0]['out_pays'] > provider_state[1]['income_docs']:
						provider_debt+=[{'name':i['name'], 'summ':i['out_pays'] - i['income_docs']}]

					if provider_state[0]['out_pays'] < provider_state[1]['income_docs']:
						provider_prepay+=[{'name':i['name'], 'summ':i['income_docs'] - i['out_pays']}]


		for buyer_state in buyers_state:
			if len(buyer_state)>1:
				for x in buyer_state:
					if buyer_state[0]['income_pays'] > buyer_state[1]['outcome_docs']:
							buyer_prepay+=[{'name':x['name'],   'summ':x['income_pays'] - x['outcome_docs']}]

					if buyer_state[0]['income_pays'] < buyer_state[1]['outcome_docs']:
						buyer_debt+=[{'name':x['name'],   'summ':x['outcome_docs'] - x['income_pays']}]

		return (provider_debt, provider_prepay, buyer_prepay, buyer_debt)
		pass

print(Hvosty("avangard.sqlite","'"+ '2016-01-30'+"'", "'"+'2018-06-01'+"'").show_contragent_balance())

