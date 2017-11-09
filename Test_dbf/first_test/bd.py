#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF
import os


dipart = 'dipartD'
avangard = 'avangard'
ditest = 'ditest'
bazi = (dipart, avangard, ditest)

location ='D:\DATA_SETS' 
t625 = location+'\{}\SC625.DBF'
t556 = location+'\{}\SC556.DBF'
t497 = location+'\{}\SC497.DBF'
t493 = location+'\{}\SC493.DBF'
t167 = location+'\{}\SC167.DBF'

lyst = (t625,t556,t497,t493,t167)

def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_data(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].replace(" ", "") ,l[args[2]].encode('latin1').decode('cp1251'), l[args[3]],l[args[4]], l[args[5]].replace(" ", "")]]
	return values_list	
	pass


def get_data_mudaki(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].encode('latin1').decode('cp1251') ,l[args[2]], l[args[3]].replace(" ", "")]]
	return values_list	
	pass


#проходится через список всех требуемых файлов-таблиц и выдергивает их. 
#превращая в листы, в внутри - создается по три варианта-листа для каждой из баз клиентов

all_t625 = [get_data_from_dbf(t625.format(i)) for i in bazi]
#all_t556 = [get_data_from_dbf(t556.format(i)) for i in bazi]
#all_t497 = [get_data_from_dbf(t497.format(i)) for i in bazi]
all_t493 = [get_data_from_dbf(t493.format(i)) for i in bazi]
all_t167 = [get_data_from_dbf(t167.format(i)) for i in bazi]


def documenty_huevy(numar, *args):
	dot = [0,1,2]
	fiat = []
	for t in dot:
		documents_table = [get_data(numar[t], args[0],args[1], args[2], args[3],args[4], args[5])]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass


def ebuchie_pidory(numar, *args):
	dot = [0,1,2]
	fiat = []
	for t in dot:
		documents_table = [get_data_mudaki(numar[t], args[0],args[1], args[2], args[3])]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass



documenty_ot_uebkov = documenty_huevy(all_t625,'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')
documenty_dlya_uebkov = documenty_huevy(all_t493,'DESCR','PARENTEXT', 'SP467', 'SP468','SP470','SP482')
mrazi =  ebuchie_pidory(all_t167, 'DESCR', 'SP134', 'SP137', 'ID')
print(len(documenty_ot_uebkov[0]))

print(len(all_t625[0]))

"""
conn1 = sqlite3.connect('1.sqlite')
conn2 = sqlite3.connect('2.sqlite')
conn3 = sqlite3.connect('3.sqlite')
c1 = conn1.cursor()
c2 = conn2.cursor()
c3 = conn3.cursor()


c1.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documenty_ot_uebkov[0])
c1.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', documenty_dlya_uebkov[0])
c1.executemany('INSERT INTO contragents VALUES (?,?,?,?)', mrazi[0])

conn1.commit()
conn1.close()
"""

"""
c2.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documenty_ot_uebkov[1])
c2.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', documenty_dlya_uebkov[1])
c2.executemany('INSERT INTO contragents VALUES (?,?,?,?)', mrazi[1])
conn2.commit()
conn2.close()


c3.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documenty_ot_uebkov[2])
c3.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', documenty_dlya_uebkov[2])
c3.executemany('INSERT INTO contragents VALUES (?,?,?,?)', mrazi[2])
conn3.commit()
conn3.close()
"""



#documents_table = get_data('contragent_documents', documents, 'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')
"""
names_table = get_data('sellers', names, 'DESCR', 'SP134', 'SP137', 'ID')
bank_data_table= get_data('contragent_bank', bank_data, 'DESCR','PARENTEXT', 'SP494', 'SP39997')
places_table= get_data('contragent_places', places, 'DESCR','PARENTEXT', 'SP24617', 'SP24618','SP24619','SP24620','SP24621','SP24622',)
"""



#SC245 - POSTAVKI



#c.executemany('INSERT INTO contragents VALUES (?,?,?,?)', names_table)
#c.executemany('INSERT INTO contragents_bank VALUES (?,?,?,?)', bank_data_table)
#c.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', documents_table)
#c.executemany('INSERT INTO contragents_places VALUES (?,?,?,?,?,?,?)', places_table)



