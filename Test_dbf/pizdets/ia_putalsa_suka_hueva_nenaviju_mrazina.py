#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF

"""
documents_from = 'SC493.dbf'
documents_to = 'SC625.dbf'
contragents_bank_data = 'SC497.dbf'
contragents_names = 'SC167.dbf'
contragents_places = 'SC556.dbf'

odinc_tables = (documents_to, documents_from, contragents_names, contragents_bank_data, contragents_places)
"""

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

all_t625 = [get_data_from_dbf(t625.format(i)) for i in bazi]
#all_t556 = [get_data_from_dbf(t556.format(i)) for i in bazi]
#all_t497 = [get_data_from_dbf(t497.format(i)) for i in bazi]
all_t493 = [get_data_from_dbf(t493.format(i)) for i in bazi]
#all_t167 = [get_data_from_dbf(t167.format(i)) for i in bazi]

def get_data(table_name, imena_stolbtsov):
	values_list = []
#	vita = [0,1,2,3,4,5]
	via = [t for t in range(len(imena_stolbtsov))]
	for l in table_name:
		values_list+=[[l[imena_stolbtsov[g]] for g in via]]
	return values_list	
	pass


dot = [0,1,2]
def another_way_to_die(numar, *args):
	urd =[ar for ar in args]
	fiat = []
	for t in dot:
		documents_table = [get_data2(numar[t], urd)]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass

#проходится через список всех требуемых файлов-таблиц и выдергивает их. 
#превращая в листы, в внутри - создается по три варианта-листа для каждой из баз клиентов



print(len(another_way_to_die(all_t625,'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')[0]))
#print(len(another_way_to_die(all_t493,'DESCR','PARENTEXT', 'SP467', 'SP468','SP470','SP482',)[2]))

docs_from = another_way_to_die(all_t625,'DESCR','PARENTEXT', 'SP609', 'SP611','SP613', 'SP617')
docs_to = another_way_to_die(all_t493,'DESCR','PARENTEXT', 'SP467', 'SP468','SP470','SP482',)



conn1 = sqlite3.connect('1.sqlite')
conn2 = sqlite3.connect('2.sqlite')
conn3 = sqlite3.connect('3.sqlite')
c1 = conn1.cursor()
c2 = conn2.cursor()
c3 = conn3.cursor()

"""
bori = ['1','2','3']

iris = [sqlite3.connect(x +'.sqlite').cursor() for x in bori]

print(iris)
"""


c1.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', docs_from[0])
c1.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', docs_to[0])
conn1.commit()
conn1.close()

"""
c2.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', docs_from[1])
c2.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', docs_to[1])
conn2.commit()
conn2.close()


c3.executemany('INSERT INTO contragents_documents VALUES (?,?,?,?,?,?)', docs_from[2])
c3.executemany('INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?)', docs_to[2])
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



