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








values_list += 
[
[

l[args[0]].encode('latin1').decode('cp1251'),
l[args[1]].encode('latin1').decode('cp1251') ,
l[args[2]], 
l[args[3]]

]
]

values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]
values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]
values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]]]]





[[b'\xcf\xce\xca\xd3\xcf\xc0\xd2\xc5\xcb\xc8'], 
[b'\xc0\xe3\xe5\xed\xf1\xf2\xf1\xf2\xe2\xee \xc2\xeb\xe0\xe4\xe8\xec\xe8\xf0\xe0 \xc3\xf0\xe5\xe2\xf6\xee\xe2\xe0'], 
[b'\xc0\xe4\xe2\xee\xea\xe0\xf2\xf1\xea\xee\xe5 \xc1\xfe\xf0\xee "\xcf\xf0\xe0\xe2\xee \xe8 \xcf\xee\xf0\xff'], 
[b'\xc0\xe9\xf0\xee\xed\xcf\xf0\xee\xe4\xe0\xea\xf8\xed \xce\xce\xce'],
  [b'\xc1\xe5\xeb\xe0\xe2\xe8\xe0 \xce\xc0\xce'], 
  [b''],
   [b'\xce\xce\xce "\xc0\xe3\xe5\xed\xf1\xf2\xf1\xf2\xe2\xee \xc2\xeb\xe0\xe4\xe8\xec\xe8\xf0\xe0 \xc3\xf0\xe5\xe2\xf6\xee\xe2\xe0"'], 
[b'\xc0\xe4\xe2\xee\xea\xe0\xf2\xf1\xea\xee\xe5 \xc1\xfe\xf0\xee "\xcf\xf0\xe0\xe2\xee \xe8 \xcf\xee\xf0\xff\xe4\xee\xea"'],
 [b'\xce\xce\xce "\xc0\xe9\xf0\xee\xed \xcf\xf0\xee\xe4\xe0\xea\xf8\xed"'],
  [b'\xce\xc0\xce "\xc0\xe2\xe8\xe0\xea\xee\xec\xef\xe0\xed\xe8\xff "\xc1\xe5\xeb\xe0\xe2\xe8\xe0 "'],
 [b''], 
 [b'100024047'],
  [b'805002493'], 
  [b'191568573'],
   [b'6000390798'], 
[b'     1'],
 [b'     2'],
  [b'     3'], 
  [b'     4'],
   [b'     5']]