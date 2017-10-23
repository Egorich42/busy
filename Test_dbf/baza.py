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

	asyra = table_name

	for l in asyra:
		values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]
	return values_list	
	pass

names = get_data_from_dbf('SC167.dbf')
#bank_data = get_data_from_dbf('SC497.dbf')
#places =  get_data_from_dbf('SC556.dbf')	

names_table = get_data('sellers', names, 'DESCR', 'SP134', 'SP137', 'ID')
#bank_data_table= get_data('contragent_bank', bank_data, 'DESCR','PARENTEXT', 'SP494', 'SP39997')
#places_table= get_data('contragent_places', places, 'DESCR','PARENTEXT', 'SP24617', 'SP24618','SP24619','SP24620','SP24621','SP24622',)


#c.executemany('INSERT INTO contragents VALUES (?,?,?,?)', names_table)
#c.executemany('INSERT INTO contragents_bank VALUES (?,?,?,?)', bank_data_table)
#c.executemany('INSERT INTO contragents_places VALUES (?,?,?,?,?,?,?)', places_table)


conn.commit()
conn.close()
values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]





