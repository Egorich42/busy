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
contragents = location+'\{}\SC167.DBF'
contragents_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137')


all_outcoming_docs = location+'\{}\SC625.DBF'
outcoming_tables = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP620')

outcoming_tn_nds = location+'\{}\DH16152.DBF'
outcoming_tn_tables = ('SP16108', 'SP16116', 'SP16139', 'SP16138', 'SP16136')

outcoming_services_nds = location+'\{}\DH3091.DBF'
outcoming_services_tables = ('SP3053', 'SP3063', 'SP3061', 'SP3060', 'SP3058')



all_incoming_docs = location+'\{}\SC493.DBF'
incoming_tables = ('DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480','SP479','SP478')

incoming_tn_nds = location+'\{}\DH14970.DBF'
incoming_tn_tables = ('SP14928', 'SP14933','SP14954', 'SP14953','SP14951')

incoming_tovary_nds = location+'\{}\DH16195.DBF'
incoming_tovary_tables = ('SP16153', 'SP16159', 'SP16184', 'SP16183', 'SP16181')

incoming_services_nds = location+'\{}\DH3050.DBF'
incoming_services_tables = ('SP3019','SP3017','SP3030', 'SP3029', 'SP3027')


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


def pred_start_list(base_name):
	contragents_list = get_contragents_list(contragents.format(base_name), contragents_tables)
	income_tovary  = get_docs_with_nds_list(incoming_tovary_nds.format(base_name), incoming_tovary_tables)
	full_income_nds = (get_docs_with_nds_list(incoming_services_nds.format(base_name), incoming_services_tables)+get_docs_with_nds_list(incoming_tn_nds.format('avangard'), incoming_tn_tables))
	full_income = get_docs_without_nds_list(all_incoming_docs.format(base_name), incoming_tables)

	full_out_nds = (get_docs_with_nds_list(outcoming_services_nds.format(base_name), outcoming_services_tables)+get_docs_with_nds_list(outcoming_tn_nds.format('avangard'), outcoming_tn_tables))
	full_out = get_docs_without_nds_list(all_outcoming_docs.format(base_name), outcoming_tables)

	return (income_tovary, full_income_nds, full_income, full_out_nds, full_out, contragents_list)
	pass



def data_sorting(income_list, data_start, data_end):
	data_borders_list = [i for i in income_list if i['doc_data'] >= data_start and  i['doc_data'] <= data_end]
	data_sorted_list = sorted(data_borders_list, key=lambda k: k['doc_data']) 
	return data_sorted_list	
	pass		


def create_documents_lists(out_list, income_list, data_start, data_end):
	outcome_serv_and_tn_list = []
	outcome_pp_list = []
	outcome_pp_vozvr = []


	income_serv_and_tn_list = []
	income_pp_list = []
	income_pp_vozvr = []
	income_pp_dpd = []

	for i in data_sorting(out_list, data_start, data_end):
		if i['del_detector'] != '*':
			if i['document_type'] != '0' and i['some_sort_one'] != '1' and i['pay_id']!= '2MS':
				outcome_serv_and_tn_list +=[i]
			if i['document_type'] == '0' and i['act_detector'] != '3':
				if i['pay_id'] == 'S5C':
					outcome_pp_vozvr += [i]
				if i['pay_id'] != 'S5C':
					outcome_pp_list += [i]	


	for i in data_sorting(income_list, data_start, data_end):
		if i['del_detector'] != '*':
			if i['document_type'] == '0' and i['some_sort_two'] != '364AS' and i['some_sort_two'] != '3649U'  :
				income_serv_and_tn_list +=[i]

			if  i['document_type'] != '0'  and i['pay_id'] !='2':
				if  i['act_detector'] =='S5B':
					income_pp_vozvr +=[i]
				if 	i['act_detector'] =='2MM':
					income_pp_dpd +=[i]
				else:
					income_pp_list += [i]
					
	return (income_serv_and_tn_list, outcome_serv_and_tn_list, income_pp_list, income_pp_vozvr, income_pp_dpd, outcome_pp_list, outcome_pp_vozvr)
	pass



def create_joined_nds_list(list_without_nds, list_with_nds,  data_start, data_end):
	new_list = []
	data_borders_list = []
	for i in list_without_nds:
		for x in list_with_nds:
			if i['parent_id'] == x['parent_id'] and  i['doc_data'] == x['doc_data'] and i['full_sum'] == x['full_sum']:
				new_list +=[{
				'document_name': i['document_name'],
				'contragent_name': i['contragent_name'],
				'doc_data': i['doc_data'],
				'full_sum': i['full_sum'],
				'nds': x['nds'],
				}]

	return data_sorting(new_list, data_start, data_end)
	pass



def return_name(docs, pp):
	name = 'default'	
	if len(pp) > 0 and len(pp) >len(docs):
		name = pp[0]['contragent_name']
	if len(docs) > 0 and len(docs) >len(pp):
		name = docs[0]['contragent_name']
	if len(docs) > 0 and len(docs) == len(pp):				
		name = docs[0]['contragent_name']
	return name	
	pass


def fin_state_sums(sum_docs, sum_pp):
	if  sum_docs == sum_pp:
		difference = 0
		message = 'все ровно'

	if sum_docs > sum_pp:
		difference = sum_docs-sum_pp
		message = 'задолженность контрагента сотавляет:'
	else:
		difference = sum_pp - sum_docs
		message = 'ваша задолженность  сотавляет:'
		
	return (difference,message)
	pass


def act_sverki(out, income, contragent_id, data_start, data_end):

	def constructor_to_sverka(number):
		result = [i for i in create_documents_lists(out, income, data_start, data_end)[number] if i['parent_id'] == contragent_id]
		return result
		pass

	income_serv_and_tn = constructor_to_sverka(0)
	income_pp = constructor_to_sverka(2)
	income_pp_vozvr = constructor_to_sverka(3)
	income_pp_dpd =  constructor_to_sverka(4)

	outcome_serv_and_tn = constructor_to_sverka(1)
	outcome_pp = constructor_to_sverka(5)
	outcome_pp_vozvr = constructor_to_sverka(6)

	income_result_pp = income_pp+income_pp_vozvr
	income_result_doc = income_serv_and_tn+income_pp_dpd

	outcome_result_pp = outcome_pp+outcome_pp_vozvr
	outcome_result_doc = outcome_serv_and_tn



	income_result_pp_sum = sum([i['full_sum'] for i in income_result_pp])
	income_result_doc_sum = sum([i['full_sum'] for i in income_result_doc])

	outcome_result_pp_sum = sum([i['full_sum'] for i in outcome_result_pp])
	outcome_result_doc_sum = sum([i['full_sum'] for i in outcome_result_doc])




income = pred_start_list('avangard')[2]
out = pred_start_list('avangard')[4]
#result = create_documents_lists(out, income,'2017-12-01', '2017-12-31')
#print(len(result[0]),len(result[1]),len(result[2]),len(result[3]),len(result[4]),len(result[5]),len(result[6]))


#print(hvosty('2017-12-01', '2017-12-31'))

act_sverki(out, income,'3CPIB','2016-06-01', '2017-12-31')
#6- AVANGARD
"""
income_tovary  = pred_start_list('avangard')[0]
income_nds = pred_start_list('avangard')[1]
income = pred_start_list('avangard')[2]

out_nds = pred_start_list('avangard')[3]
out = pred_start_list('avangard')[4]

vhod_nds = round(sum([i['nds'] for i in create_joined_nds_list(create_documents_lists(out,income, '2017-12-01', '2017-12-31')[0], income_nds, '2017-12-01', '2017-12-31')]),2)
ishod_nds = round(sum([i['nds'] for i in create_joined_nds_list(create_documents_lists(out, income,'2017-12-01', '2017-12-31')[1], out_nds, '2017-12-01', '2017-12-31')]),2)
nds_tovary = round(sum([i['nds'] for i in data_sorting(income_tovary,'2017-12-01', '2017-12-31')]),2)
"""




#print(vhod_nds)
#print(ishod_nds)
#print(nds_tovary)

"""
def hvosty(data_start, data_end):
	hvosty_list = []

	debts_providers=[]
	prepayment_providers=[]
	debts_buyers=[]
	prepayment_buyers=[]

	for i in [x['contragent_id'] for x in pred_start_list('avangard')[5]]:
		if act_sverki(out, income, i, data_start, data_end)[4] > 0.5 and len(act_sverki(out, income, i, data_start, data_end)[0]) > 0:
			hvosty_list += [{'difference': round(act_sverki(out, income, i, data_start, data_end)[4],2), 'name':act_sverki(out, income,i, data_start, data_end)[6] }]

	return 	hvosty_list
	pass
"""