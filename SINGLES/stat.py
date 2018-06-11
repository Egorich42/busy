from forge import sqlite3, create_list_of_table_values, outcome_serv_nds, outcome_tn_nds, income_serv_nds, income_tn_nds, income_tovary,outcome_full_nonds

class CompanyBalance:
	def __init__(self, base_name = None, data_start = None, data_end = None):
		self.base_name = base_name
		self.data_start = data_start
		self.data_end = data_end


	def tax_sum(self, select_command, cursor, tax_type):
		return sum([float(x[tax_type]) for x in create_list_of_table_values(cursor.execute(select_command.format(self.data_start, self.data_end)),cursor.description) if x[tax_type] != None])


	def count_nds(self):
		conn = sqlite3.connect(self.base_name)
		cur = conn.cursor()
		outcome_nds_sum = self.tax_sum(outcome_serv_nds, cur, 'nds')+self.tax_sum(outcome_tn_nds, cur, 'nds')
		income_nds_sum = self.tax_sum(income_serv_nds, cur, 'nds')+self.tax_sum(income_tn_nds, cur, 'nds')+self.tax_sum(income_tovary, cur, 'nds')
 
		conn.commit()
		conn.close()		

		return (outcome_nds_sum, income_nds_sum, outcome_nds_sum - income_nds_sum)
		pass


	def count_usn(self):
		conn = sqlite3.connect(self.base_name)
		cur = conn.cursor()
		usn_sum = round(self.tax_sum(outcome_full_nonds, cur, 'summ')*0.05, 2)
 
		conn.commit()
		conn.close()

		return usn_sum
		pass

print(CompanyBalance('DipartD.sqlite', "'2018-01-01'", "'2018-03-31'").count_usn())


