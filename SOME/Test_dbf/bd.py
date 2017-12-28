#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF
import os
import sql_commands as sq_c

bazi = ('dipartD', 'avangard', 'ditest','bus','centrupakovki','ipmatusev','mitada', 'smdpark','komikHS','himbaza','belwestagro')

location ='D:\DATA_SETS' 
t625 = location+'\{}\SC625.DBF'
t556 = location+'\{}\SC556.DBF'
t497 = location+'\{}\SC497.DBF'
t493 = location+'\{}\SC493.DBF'
t167 = location+'\{}\SC167.DBF'
t38349 = location+'\{}\SC38349.DBF'
t37440 = location+'\{}\SC37440.DBF'
t37454 = location+'\{}\SC37454.DBF'


#lyst = (t625,t556,t497,t493,t167,t38349,t37440,t37454)

def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_data(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].replace(" ", ""),l[args[2]].replace(" ", "") ,l[args[3]].encode('latin1').decode('cp1251'), l[args[4]],l[args[5]], l[args[6]].replace(" ", ""),l[args[7]].replace(" ", ""),str(l[args[8]]).replace(" ", ""),str(l[args[9]]).replace(" ", "")]]
	return values_list	
	pass

def get_data_mudaki(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].replace(" ", ""), l[args[1]].encode('latin1').decode('cp1251'),l[args[2]].replace(" ", "") ,l[args[3]].encode('latin1').decode('cp1251'), l[args[4]].replace(" ", "")]]
	return values_list	
	pass


#проходится через список всех требуемых файлов-таблиц и выдергивает их. 
#превращая в листы, в внутри - создается по три варианта-листа для каждой из баз клиентов

all_t625 = [get_data_from_dbf(t625.format(i)) for i in bazi]
#all_t556 = [get_data_from_dbf(t556.format(i)) for i in bazi]
#all_t497 = [get_data_from_dbf(t497.format(i)) for i in bazi]
all_t493 = [get_data_from_dbf(t493.format(i)) for i in bazi]
all_t167 = [get_data_from_dbf(t167.format(i)) for i in bazi]


all_t38349 = [get_data_from_dbf(t38349.format(i)) for i in bazi]
all_t37440 = [get_data_from_dbf(t37440.format(i)) for i in bazi] 
all_t37454 = [get_data_from_dbf(t37454.format(i)) for i in bazi]


#SC245 - товары, похоже
#SC173 - DOGOVORA
#SC199 - вероятно, это покупки
#SC309 - 
#SC368 - список сотрудников
#SC505 - спиок банков
#SC591 - список профессий
#DH1294, DH1310 - узнать, что за оно


#Sc 38349, 3745437440
#18687   SC22163  SC 245

def documenty_list(numar, *args):
	dot = range(len(bazi))
	fiat = []
	for t in dot:
		documents_table = [get_data(numar[t], args[0],args[1], args[2], args[3],args[4],args[5], args[6],args[7],args[8],args[9])]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass

def contragents_list(numar, *args):
	dot = range(len(bazi))
	fiat = []
	for t in dot:
		documents_table = [get_data_mudaki(numar[t], args[0], args[1], args[2],args[3], args[4])]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass


documenty_dlya_contragentov= documenty_list(all_t625,'DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619')
documenty_ot_contragentov = documenty_list(all_t493,'DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480')

#eschf_inner = documenty_list(all_t37440,'ID','DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480')


contragenty =  contragents_list(all_t167, 'ID','DESCR', 'ISMARK','SP134', 'SP137')

def update_from_dbf(dbf_list, sq_command,db_number, insert_command):
	conn = sqlite3.connect(str(db_number)+'.sqlite')
	cur = conn.cursor()
	sql_data = (cur.execute(sq_command).fetchall())
	print(len(sql_data))
	result = len(dbf_list)-len(sql_data)
	if result > 0:
		vnos_obnovlenia = dbf_list[-result:]
		print(len(vnos_obnovlenia))
		cur.executemany(insert_command, vnos_obnovlenia)
		conn.commit()
		conn.close()
		print()	

	pass

def full_update(list_number, base_number):
	update_from_dbf(documenty_dlya_contragentov[list_number],sq_c.select_all_documents,base_number,sq_c.insert_into_docs)
	update_from_dbf(documenty_ot_contragentov[list_number],sq_c.select_all_documents_two,base_number,sq_c.insert_into_docs_two)
	update_from_dbf(contragenty[list_number],sq_c.select_contragents,base_number,sq_c.insert_into_contragents)
	pass


for i in [1,2,3,4,5,6,7,8,9,10,11]:
	full_update(i-1,i)
