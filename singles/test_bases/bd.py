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


location ='D:\DATA_SETS' 
t625 = location+'\{}\SC625.DBF'
t625_tables_names = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP620')

t493 = location+'\{}\SC493.DBF'
t493_tables_names = ('DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480','SP479','SP478')

t167 = location+'\{}\SC167.DBF'
t167_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137')

t625_tn_nds = location+'\{}\DH16152.DBF'
t625_tn_nds_tables = ('SP16108', 'SP16116', 'SP16139', 'SP16138', 'SP16136')

t625_uslugi_nds = location+'\{}\DH3091.DBF'
t625_uslugi_nds_tables = ('SP3053', 'SP3063', 'SP3061', 'SP3060', 'SP3058')

t493_uslugi_nds = location+'\{}\DH3050.DBF'
t493_uslugi_nds_tables = ('SP3019','SP3017','SP3030', 'SP3029', 'SP3027')

t493_tn_nds = location+'\{}\DH14970.DBF'
t493_tn_nds_tables = ('SP14928', 'SP14933','SP14954', 'SP14953','SP14951')


incoming_tovary_nds = location+'\{}\DH16195.DBF'
incoming_tovary_tables = ('SP16153', 'SP16159', 'SP16184', 'SP16183', 'SP16181')



def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_docs_with_nds(from_dbf_table, tables_names):
	values_list = []
	for i in from_dbf_table:	
		values_list += [(str(dict(i)[tables_names[0]]).replace(" ", ""),dict(i)[tables_names[1]],dict(i)[tables_names[2]],
						dict(i)[tables_names[3]],dict(i)[tables_names[4]])]
	return values_list	
	pass


def get_data(from_dbf_table,tables_names):
	values_list = []
	for i in from_dbf_table:
		values_list += [
						(
						dict(i)[tables_names[0]].encode('latin1').decode('cp1251'),
						dict(i)[tables_names[1]].replace(" ", ""),
						dict(i)[tables_names[2]].replace(" ", ""),
						dict(i)[tables_names[3]].encode('latin1').decode('cp1251'), 
						dict(i)[tables_names[4]],
						dict(i)[tables_names[5]], 
						dict(i)[tables_names[6]].replace(" ", ""),
						dict(i)[tables_names[7]].replace(" ", ""),
						str(dict(i)[tables_names[8]]).replace(" ", ""),
						str(dict(i)[tables_names[9]]).replace(" ", ""),
						dict(i)[tables_names[10]],
						dict(i)[tables_names[11]].replace(" ", ""),
						)
						]
	return values_list	
	pass



def get_data_mudaki(from_dbf_table, tables_names):
	values_list = []
	for i in from_dbf_table:
		values_list += [(
						dict(i)[tables_names[0]].replace(" ", ""),
						dict(i)[tables_names[1]].encode('latin1').decode('cp1251'),
						dict(i)[tables_names[2]].replace(" ", ""),
						dict(i)[tables_names[3]].encode('latin1').decode('cp1251'), 
						dict(i)[tables_names[4]].replace(" ", "")
						)]						
	return values_list	
	pass


def create_list_base_tables():
	big_tables_list = []
	for x in (t625,t493, t167,t625_uslugi_nds,t625_tn_nds, t493_uslugi_nds, t493_tn_nds,incoming_tovary_nds):
		tables_in_bases = [get_data_from_dbf(x.format(i)) for i in bazi]

		big_tables_list +=[tables_in_bases]
	return	big_tables_list
	pass




def create_docs_list(numar, table_names):
	fiat = []
	for t in range(len(bazi)):
		documents_table = [get_docs_with_nds(numar[t], table_names)]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass



contragenty =  create_docs_list(create_list_base_tables()[2],t167_tables)

documenty_dlya_contragentov= create_docs_list(create_list_base_tables()[0],t625_tables_names)
documenty_ot_contragentov = create_docs_list(create_list_base_tables()[1],t493_tables_names)

uslygi_okazany =  create_docs_list(create_list_base_tables()[3], t625_uslugi_nds_tables )
nakladnye =  create_docs_list(create_list_base_tables()[4], t625_tn_nds_tables )

uslygi_polychenye =  create_docs_list(create_list_base_tables()[5], t493_uslugi_nds_tables)
nakladnye_polychenye =  create_docs_list(create_list_base_tables()[6], t493_tn_nds_tables)
 
tovary_polychenye = create_docs_list(create_list_base_tables()[7], incoming_tovary_tables) 

def update_from_dbf(dbf_list, sq_command,db_number, insert_command):
	conn = sq_c.sqlite3.connect(root_path+'\\'+'sql_db'+'\\'+str(db_number)+'.sqlite')
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
	pass



def full_update(list_number, base_number):
	update_from_dbf(documenty_dlya_contragentov[list_number],sq_c.select_all_documents,base_number,sq_c.insert_into_docs)
	update_from_dbf(documenty_ot_contragentov[list_number],sq_c.select_all_documents_two,base_number,sq_c.insert_into_docs_two)
	update_from_dbf(contragenty[list_number],sq_c.select_contragents,base_number,sq_c.insert_into_contragents)

	update_from_dbf(uslygi_okazany[list_number],sq_c.select_all_ishod_nds_usl,base_number,sq_c.insert_usl_okaz_nds)
	update_from_dbf(nakladnye[list_number],sq_c.select_all_ishod_nds_tn,base_number,sq_c.insert_tn_otpravl_nds)

	update_from_dbf(uslygi_polychenye[list_number],sq_c.select_all_vhod_nds_usl,base_number,sq_c.insert_usl_poluch_nds)
	update_from_dbf(nakladnye_polychenye[list_number],sq_c.select_all_vhod_nds_tn,base_number,sq_c.insert_tn_vhod_nds)

	update_from_dbf(tovary_polychenye[list_number],sq_c.select_all_tovary,base_number,sq_c.insert_tovary)
	pass


for i in range(len(bazi)):
	full_update(i,i+1)
	pass


#SC245 - товары, похоже
#SC173 - DOGOVORA
#SC199 - вероятно, это покупки
#SC309 - 
#SC368 - список сотрудников
#SC505 - спиок банков
#SC591 - список профессий
#DH1294, DH1310 - узнать, что за оно

#DH3050, DH32635 - акты
#Sc 38349, 374543, 7440
#18687   SC22163  
#37749