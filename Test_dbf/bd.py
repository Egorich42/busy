#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF
conn = sqlite3.connect('contragents.sqlite')
c = conn.cursor()


def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_data(values_list, table_name, *args):
	values_list = []
	for l in table_name:
		if len(args) == 4:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]
		if len(args) == 6:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]] ,l[args[2]].encode('latin1').decode('cp1251'), l[args[3]],l[args[4]]]]
		if len(args) > 6:
			values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]] ,l[args[2]],l[args[3]].encode('latin1').decode('cp1251'),l[args[4]].encode('latin1').decode('cp1251'),l[args[5]].encode('latin1').decode('cp1251'),l[args[6].encode('latin1').decode('cp1251')]]]
	return values_list	
	pass

documents = get_data_from_dbf('SC625.dbf')
names = get_data_from_dbf('SC167.dbf')
bank_data = get_data_from_dbf('SC497.dbf')
places =  get_data_from_dbf('SC556.dbf')	

names_table = get_data('sellers', names, 'DESCR', 'SP134', 'SP137', 'ID')
bank_data_table= get_data('contragent_bank', bank_data, 'DESCR','PARENTEXT', 'SP494', 'SP39997')
places_table= get_data('contragent_places', places, 'DESCR','PARENTEXT', 'SP24617', 'SP24618','SP24619','SP24620','SP24621','SP24622',)
documents_table = get_data('contragent_documents', documents, 'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')





c.executemany('INSERT INTO contragents VALUES (?,?,?,?)', names_table)
c.executemany('INSERT INTO contragents_bank VALUES (?,?,?,?)', bank_data_table)
c.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?)', documents_table)
c.executemany('INSERT INTO contragents_places VALUES (?,?,?,?,?,?,?)', places_table)

conn.commit()
conn.close()

