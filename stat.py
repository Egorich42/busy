from TESTO import sqlite3, create_list_of_table_values, outcome_serv_nds, outcome_tn_nds, income_serv_nds, income_tn_nds, income_tovary

class CompanyBalance:
	def __init__(self, base_name = None, data_start = None, data_end = None):
		self.base_name = base_name
		self.data_start = data_start
		self.data_end = data_end




	def count_nds(self):
		connect = sqlite3.connect(self.base_name)
		cursor = connect.cursor()
		outcome_nds_sum = sum([float(x['nds']) for x in create_list_of_table_values(cursor.execute(outcome_serv_nds),cursor.description) if x['nds'] != None]) +  sum([float(x['nds']) for x in create_list_of_table_values(cursor.execute(outcome_tn_nds),cursor.description) if x['nds'] != None])
		income_nds_sum = sum([float(x['nds']) for x in create_list_of_table_values(cursor.execute(income_serv_nds),cursor.description) if x['nds'] != None]) +  sum([float(x['nds']) for x in create_list_of_table_values(cursor.execute(income_tn_nds),cursor.description) if x['nds'] != None])+sum([float(x['nds']) for x in create_list_of_table_values(cursor.execute(income_tovary),cursor.description) if x['nds'] != None])

		outcome_nds_sum - income_nds_sum

		connect.commit()
		connect.close()
		return (outcome_nds_sum, income_nds_sum, outcome_nds_sum - income_nds_sum)
		pass





print(CompanyBalance('avangard.sqlite').count_nds())

#[i for i in list_ishod_nds_tn+list_ishod_nds_usl if i['nds'] != 0.0 and i['nds']!=None]