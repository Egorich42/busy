#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import sys
path_to_file = os.path.dirname(os.path.abspath(__file__))+'\\'
convert_to_list = path_to_file.split('\\')[:-2]
root_path = '\\'.join(convert_to_list)
sys.path.append(root_path)
import sql_commands as sq_c
from dbfread import DBF


bazi = ('dipartD', 'avangard', 'ditest','ipmatusev','mitada', 'smdpark','himprom_den', 'polymia_den')
"""
SC625 - исходящие (накладные, акты, платежки)
SC493 - входящие(приход улуг и материалов)
SC167 - контрагенты

DH16152 - материалы входящие с НДС
DH3091 - услуги входящие с НДС

DH14970 - накладные отправленные
DH3050 - услуги оказанные
"""
location ='D:\DATA_SETS' 
all_outcoming_docs = location+'\{}\SC625.DBF'
outcoming_tables = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP620')

all_incoming_docs = location+'\{}\SC493.DBF'
incoming_tables = ('DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480','SP479','SP478')

contragents = location+'\{}\SC167.DBF'
contragents_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137')


incoming_tn_nds = location+'\{}\DH16152.DBF'
incoming_tn_tables = ('SP16108', 'SP16116', 'SP16139', 'SP16138', 'SP16136')

incoming_services_nds = location+'\{}\DH3091.DBF'
incoming_services_tables = ('SP3053', 'SP3063', 'SP3061', 'SP3060', 'SP3058')


outcoming_tn_nds = location+'\{}\DH14970.DBF'
outcoming_tn_tables = ('SP14928', 'SP14933','SP14954', 'SP14953','SP14951')

outcoming_services_nds = location+'\{}\DH3050.DBF'
outcoming_services_tables = ('SP3019','SP3017','SP3030', 'SP3029', 'SP3027')


def get_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_docs_with_nds_list(table_name, tables_names):
	values_list = []
	for i in get_from_dbf(table_name):	
		values_list += [{
						'parent_id': str(dict(i)[tables_names[0]]).replace(" ", ""),
						'doc_data':str(dict(i)[tables_names[1]]),
						'full_sum': dict(i)[tables_names[2]],
						'nds':dict(i)[tables_names[3]],
						'bez_ndz': dict(i)[tables_names[4]]
						}]
	return values_list	
	pass



def get_contragents_list(table_name, tables_names):
	values_list = []
	for i in get_from_dbf(table_name):	
		values_list += [{
						'contragent_id': str(dict(i)[tables_names[0]]).replace(" ", ""),
						'name': dict(i)[tables_names[1]].encode('latin1').decode('cp1251'),
						'deleted': dict(i)[tables_names[2]].replace(" ", "") ,
						'full_name': dict(i)[tables_names[3]].encode('latin1').decode('cp1251'),
						'unp': dict(i)[tables_names[4]].replace(" ", "")
						}]
	return values_list	
	pass



def get_docs_without_nds_list(table_name, tables_names):
	values_list = []
	for i in get_from_dbf(table_name):
		values_list += [{
						'document_name': dict(i)[tables_names[0]].encode('latin1').decode('cp1251'),
						'parent_id': dict(i)[tables_names[1]].replace(" ", ""),
						'del_detector': dict(i)[tables_names[2]].replace(" ", ""),
						'contragent_name': dict(i)[tables_names[3]].encode('latin1').decode('cp1251'), 
						'doc_data': str(dict(i)[tables_names[4]]),
						'full_sum': dict(i)[tables_names[5]],
						'document_type': dict(i)[tables_names[6]].replace(" ", ""),
						'del_detector_two': dict(i)[tables_names[7]].replace(" ", ""),
						'act_detector': str(dict(i)[tables_names[8]]).replace(" ", ""),
						'pay_id': str(dict(i)[tables_names[9]]).replace(" ", ""),
						'some_sort_one': dict(i)[tables_names[10]],
						'some_sort_two': dict(i)[tables_names[11]].replace(" ", ""),
						}]

	return values_list	
	pass

out_nds = (get_docs_with_nds_list(incoming_services_nds.format('avangard'), incoming_services_tables)+get_docs_with_nds_list(incoming_tn_nds.format('avangard'), incoming_tn_tables))
out = get_docs_without_nds_list(all_outcoming_docs.format('avangard'), outcoming_tables)

def tn_list():
	tn_list = []
	for i in out:
		if i['del_detector'] != '*' and i['document_type'] != '0' and i['some_sort_one'] != '1' and i['pay_id']!= '2MS':
			tn_list +=[i]
	return tn_list

print(len(tn_list()))


def nds_list():
	new_list = []
	without_nds = []
	for i in tn_list():
		for x in out_nds:
			if i['parent_id'] == x['parent_id'] and  i['doc_data'] == x['doc_data'] and i['full_sum'] == x['full_sum']:
				new_list +=[{
				'document_name': i['document_name'],
				'contragent_name': i['contragent_name'],
				'doc_data': i['doc_data'],
				'full_sum': i['full_sum'],
				'nds': x['nds'],
				}]
			else:
				without_nds[i]
				

	return new_list				
print(nds_list()[234])
