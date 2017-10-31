#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF
import os
#conn = sqlite3.connect('1.sqlite')
#c = conn.cursor()


documents_from = 'SC493.dbf'
documents_to = 'SC625.dbf'
contragents_bank_data = 'SC497.dbf'
contragents_names = 'SC167.dbf'
contragents_places = 'SC556.dbf'

odinc_tables = (documents_to, documents_from, contragents_names, contragents_bank_data, contragents_places)

"""
def get_data_from_dbf2(table_name):
	datasets = [list(DBF(dataset, encoding='iso-8859-1')) for dataset in odinc_tables]
	return datasets
	pass
"""



def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass



def get_data(values_list, table_name, *args):
	values_list = []
	for l in table_name:
		if len(args) == 4:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]].replace(" ", "")]]
		if len(args) == 6:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].replace(" ", "") ,l[args[2]].encode('latin1').decode('cp1251'), l[args[3]],l[args[4]], l[args[5]].replace(" ", "")]]
		if len(args) > 6:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]] ,l[args[2]],l[args[3]].encode('latin1').decode('cp1251'),l[args[4]].encode('latin1').decode('cp1251'),l[args[5]].encode('latin1').decode('cp1251'),l[args[6].encode('latin1').decode('cp1251')]]]
	return values_list	
	pass

a = os.path.basename('dipartD\SC625.dbf')
print(a)
b = os.path.exists('1c\dipartD\SC625.DBF')
v = os.path.isfile('dipartD\SC625.DBF')
print(v,b)
#documents = get_data_from_dbf(a)

"""
documents = get_data_from_dbf('SC625.dbf')
documents_table = get_data('contragent_documents', documents, 'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')

names = get_data_from_dbf('SC167.dbf')
bank_data = get_data_from_dbf('SC497.dbf')
places =  get_data_from_dbf('SC556.dbf')	


names_table = get_data('sellers', names, 'DESCR', 'SP134', 'SP137', 'ID')
bank_data_table= get_data('contragent_bank', bank_data, 'DESCR','PARENTEXT', 'SP494', 'SP39997')
places_table= get_data('contragent_places', places, 'DESCR','PARENTEXT', 'SP24617', 'SP24618','SP24619','SP24620','SP24621','SP24622',)
"""



base_numbers = ['1', '2', '3']

for i in base_numbers:
	conn = sqlite3.connect(i+'.sqlite')
	c = conn.cursor()
	#c.executemany('INSERT INTO contragents VALUES (?,?,?,?)', names_table)
	#c.executemany('INSERT INTO contragents_bank VALUES (?,?,?,?)', bank_data_table)
	#c.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documents_table)
	#c.executemany('INSERT INTO contragents_places VALUES (?,?,?,?,?,?,?)', places_table)
	#conn.commit()
	#conn.close()


#SC245 - POSTAVKI


"""
[get_data_from_dbf('SC625.dbf') for bit in odinc_tables]

documents = get_data_from_dbf('SC625.dbf')
names = get_data_from_dbf('SC167.dbf')
bank_data = get_data_from_dbf('SC497.dbf')
places =  get_data_from_dbf('SC556.dbf')	


names_table = get_data('sellers', names, 'DESCR', 'SP134', 'SP137', 'ID')
bank_data_table= get_data('contragent_bank', bank_data, 'DESCR','PARENTEXT', 'SP494', 'SP39997')
places_table= get_data('contragent_places', places, 'DESCR','PARENTEXT', 'SP24617', 'SP24618','SP24619','SP24620','SP24621','SP24622',)
documents_table = get_data('contragent_documents', documents, 'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')

"""



#c.executemany('INSERT INTO contragents VALUES (?,?,?,?)', names_table)
#c.executemany('INSERT INTO contragents_bank VALUES (?,?,?,?)', bank_data_table)
#c.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documents_table)
#c.executemany('INSERT INTO contragents_places VALUES (?,?,?,?,?,?,?)', places_table)

conn.commit()
conn.close()

