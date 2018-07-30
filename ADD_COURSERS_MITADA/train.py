from hand_updater import get_today_courses
import sqlite3
import dbf
from datetime import date


select_course_data = """
SELECT * FROM rates
WHERE rates.data={}
AND rates.name = {}
ORDER BY rates.data;
"""

class Updater:
	def __init__(self, base_name = None):
		self.base_name = base_name
		self.valute_info = dbf.Table('{}/SC122'.format(self.base_name), codepage='cp1251')
		self.dbf_val_table = dbf.Table('{}/1SCONST'.format(self.base_name), codepage='cp1251')


	def get_dbf_valute(self):
		self.valute_info.open()
		values_list = []
		for info in self.valute_info:
			if info.ismark != '*' and info.descr != 'BYN':
				values_list += [{'descr':info.descr, 'id':info.id}]
		self.valute_info.close()

		return values_list



	def courses_selector(self, val_name):
		conn = sqlite3.connect('courses.sqlite')
		cur = conn.cursor()
		ad = cur.execute(select_course_data.format('"'+str(date.today())+'"', '"'+str(val_name)+'"') ).fetchone()
		conn.commit()
		conn.close()
		return ad

	def get_today_course(self):
		courses_list = []
		courses_list_two = []
		for x in self.get_dbf_valute():
			cours_cell = self.courses_selector(x['descr'])
			if cours_cell != None: 
				courses_list += [(x['id'],'U4Y', date.today(),0, str(cours_cell[3]), '0','0','0','0', None )]
				courses_list_two += [(x['id'],'3A', date.today(),0, str(cours_cell[2]), '0','0','0','0', None )]
		return (courses_list, courses_list_two)
		pass



	def update_dbf_file(self):
		self.dbf_val_table.open()

		for course in self.get_today_course()[0]:
			self.dbf_val_table.append(course)

		for course_mult in self.get_today_course()[1]:
			self.dbf_val_table.append(course_mult)

		self.dbf_val_table.close()
		pass

for x in ('zeno', 'mitada', 'amedenta','matusev'):
	Updater(x).update_dbf_file()