#! /usr/bin/env python
# -*- coding: utf-8 -*

#------!!!pip install -----!
import sqlite3
from dbfread import DBF
import os
from .models import *

bazi = ('dipartD', 'avangard', 'ditest','bus','centrupakovki','ipmatusev','mitada')

location ='D:\DATA_SETS' 
t625 = location+'\{}\SC625.DBF'
t493 = location+'\{}\SC493.DBF'
t167 = location+'\{}\SC167.DBF'

lyst = (t625,t493,t167)

def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_data(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].encode('latin1').decode('cp1251'),l[args[1]].replace(" ", ""),l[args[2]].replace(" ", "") ,l[args[3]].encode('latin1').decode('cp1251'), l[args[4]],l[args[5]], l[args[6]].replace(" ", ""),l[args[7]].replace(" ", ""),l[args[8]]]]
	return values_list	
	pass


def get_data_mudaki(table_name, *args):
	values_list = []
	for l in table_name:
		values_list += [[l[args[0]].replace(" ", ""), l[args[1]].encode('latin1').decode('cp1251'),l[args[2]].replace(" ", "") ,l[args[3]].encode('latin1').decode('cp1251'), l[args[4]].replace(" ", "")]]
	return values_list	
	pass

all_t625 = [get_data_from_dbf(t625.format(i)) for i in bazi]
all_t493 = [get_data_from_dbf(t493.format(i)) for i in bazi]
all_t167 = [get_data_from_dbf(t167.format(i)) for i in bazi]


def documenty_list(numar, *args):
	dot = range(len(bazi))
	fiat = []
	for t in dot:
		documents_table = [get_data(numar[t], args[0],args[1], args[2], args[3],args[4],args[5], args[6],args[7],args[8])]
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


documenty_dlya_contragentov= documenty_list(all_t625,'DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615')
documenty_ot_contragentov = documenty_list(all_t493,'DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP15435')
contragenty =  contragents_list(all_t167, 'ID','DESCR', 'ISMARK','SP134', 'SP137')



def update_from_dbf(dbf_list, sq_command,db_number, insert_command):
	conn = sqlite3.connect(str(db_number)+'.sqlite')
	cur = conn.cursor()
	sql_data = (cur.execute(sq_command).fetchall())
	result = len(dbf_list)-len(sql_data)
	if result > 0:
		vnos_obnovlenia = dbf_list[-result:]
		cur.executemany(insert_command, vnos_obnovlenia)
		conn.commit()
		conn.close()
	pass

def full_update(list_number, base_number):
	update_from_dbf(documenty_dlya_contragentov[list_number],sq_c.select_all_documents,base_number,sq_c.insert_into_docs)
	update_from_dbf(documenty_ot_contragentov[list_number],sq_c.select_all_documents_two,base_number,sq_c.insert_into_docs_two)
	update_from_dbf(contragenty[list_number],sq_c.select_contragents,base_number,sq_c.insert_into_contragents)
	pass
