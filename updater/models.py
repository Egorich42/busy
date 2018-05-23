from django.db import models
import sqlite3 
from dbfread import DBF
import os.path



select_all = "SELECT * FROM {};"
insert_into = "INSERT INTO {} VALUES {};"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


f = open(BASE_DIR+'\\'+'bases.txt')
bazi = [line.split(',') for line in f][0]


t625 = BASE_DIR+'\{}\SC625.DBF'
t625_tables_names = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP616', 'SP620')

t493 = BASE_DIR+'\{}\SC493.DBF'
t493_tables_names = ('DESCR','PARENTEXT','ISMARK','SP467', 'SP468','SP470', 'SP482','VERSTAMP','SP479','SP482', 'SP478','SP480', 'SP476')

t167 = BASE_DIR+'\{}\SC167.DBF'
t167_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137','SP155')

t625_tn_nds = BASE_DIR+'\{}\DH16152.DBF'
t625_tn_nds_tables = ('SP16108', 'SP16116', 'SP16139', 'SP16138', 'SP16136')

t625_uslugi_nds = BASE_DIR+'\{}\DH3091.DBF'
t625_uslugi_nds_tables = ('SP3053', 'SP3063', 'SP3061', 'SP3060', 'SP3058')

t493_uslugi_nds = BASE_DIR+'\{}\DH3050.DBF'
t493_uslugi_nds_tables = ('SP3019','SP3017','SP3030', 'SP3029', 'SP3027')

t493_tn_nds = BASE_DIR+'\{}\DH14970.DBF'
t493_tn_nds_tables = ('SP14928', 'SP14933','SP14954', 'SP14953','SP14951')


incoming_tovary_nds = BASE_DIR+'\{}\DH16195.DBF'
incoming_tovary_tables = ('SP16153', 'SP16159', 'SP16184', 'SP16183', 'SP16181')


countries = BASE_DIR+'\{}\SC576.DBF'
countries_tables = ('ID','CODE','DESCR','SP574','SP33760')


currency = BASE_DIR+'\{}\SC114.DBF'
currency_tables = ('ID', 'CODE','DESCR','SP105')



contragents_colls =          '(id, name, deleted, full_name, unp, country)'
contragents_docs_colls =     '(document_name, parent, deleted, contragent_name, doc_date, summ, doc_type, del_counter, operation_type, pay_type, back_flag,             currency_type, account_type)'
contragents_docs_two_colls = '(document_name, parent, deleted, contragent_name, doc_date, summ, doc_type, del_counter, operation_type, pay_type, provider_account_type, currency_type, document)'
nds_docs_colls =             '(parent, data, full_sum, nds, bez_nds)'
countries_colls =            '(dbf_id, code, name, country_type, ts_marker)'
currency_colls =             '(dbf_id, code, name, currency_id)'



contragents_data = {'table_name': 'contragents', 'coll_names':contragents_colls, 'insert_values':'(?,?,?,?,?,?)'}
contragents_docs_data = {'table_name':  'contragents_documents', 'coll_names':contragents_docs_colls, 'insert_values': '(?,?,?,?,?,?,?,?,?,?,?,?,?)' }
contragents_docs_two_data = {'table_name':  'contragents_documents_two', 'coll_names':contragents_docs_two_colls, 'insert_values': '(?,?,?,?,?,?,?,?,?,?,?,?,?)' }
ishod_nds_tn_data = {'table_name':'ishod_nds_tn', 'coll_names':nds_docs_colls, 'insert_values':'(?,?,?,?,?)' }
ishod_nds_usl_data = {'table_name':'ishod_nds_usl', 'coll_names':nds_docs_colls, 'insert_values':'(?,?,?,?,?)' }
nds_tovary_data = {'table_name':'nds_tovary', 'coll_names':nds_docs_colls, 'insert_values':'(?,?,?,?,?)'}
vhod_nds_tn_data = {'table_name':'vhod_nds_tn', 'coll_names':nds_docs_colls, 'insert_values':'(?,?,?,?,?)' }
vhod_nds_usl_data = {'table_name':'vhod_nds_usl', 'coll_names':nds_docs_colls, 'insert_values': '(?,?,?,?,?)'}

countries_data = {'table_name': 'countries', 'coll_names': countries_colls, 'insert_values':'(?,?,?,?,?)' }
currency_data = {'table_name': 'currency',  'coll_names': currency_colls, 'insert_values':'(?,?,?,?)' }


def get_data_from_dbf(table_name):
    dataset = list(DBF(table_name, encoding='iso-8859-1'))
    return dataset
    pass


def tranform_from_dbf(from_dbf_table, tables_names):
    values_list = []
    for i in from_dbf_table:  
        values_list += [[str(dict(i)[x]).encode('latin1').decode('cp1251').strip() for x in tables_names]]
    return values_list  
    pass



def create_list_base_tables():
    big_tables_list = []
    for x in (t625, t493, t167, t625_uslugi_nds, t625_tn_nds, t493_uslugi_nds, t493_tn_nds, incoming_tovary_nds, countries, currency):
        big_tables_list += [[get_data_from_dbf(x.format(i)) for i in bazi]]
    return  big_tables_list
    pass



def create_tranformed_list(numar, table_names):
    fiat = []
    for t in range(len(bazi)):
        documents_table = [tranform_from_dbf(numar[t], table_names)]
        fiat += [ti for ti in documents_table]
    return fiat 
    pass




def update_from_dbf(dbf_list, sq_command,db_number, table, insert_command):
    conn = sqlite3.connect(BASE_DIR+'\\'+'sqlite_bases'+'\\'+str(db_number)+'.sqlite')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table['table_name'], table['coll_names']))

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
    
    update_from_dbf(create_tranformed_list(create_list_base_tables()[2], t167_tables)[list_number], select_all.format(contragents_data['table_name']), base_number, contragents_data, insert_into.format(contragents_data['table_name'], contragents_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[0], t625_tables_names)[list_number], select_all.format(contragents_docs_data['table_name']), base_number, contragents_docs_data, insert_into.format(contragents_docs_data['table_name'], contragents_docs_data['insert_values']))
    update_from_dbf(create_tranformed_list(create_list_base_tables()[1], t493_tables_names)[list_number], select_all.format(contragents_docs_two_data['table_name']), base_number, contragents_docs_two_data, insert_into.format(contragents_docs_two_data['table_name'], contragents_docs_two_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[3], t625_uslugi_nds_tables )[list_number], select_all.format(ishod_nds_usl_data['table_name']), base_number, ishod_nds_usl_data, insert_into.format(ishod_nds_usl_data['table_name'], ishod_nds_usl_data['insert_values']))
    update_from_dbf(create_tranformed_list(create_list_base_tables()[4], t625_tn_nds_tables )[list_number], select_all.format(ishod_nds_tn_data['table_name']), base_number, ishod_nds_tn_data, insert_into.format(ishod_nds_tn_data['table_name'], ishod_nds_tn_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[5], t493_uslugi_nds_tables)[list_number], select_all.format(vhod_nds_usl_data['table_name']), base_number, vhod_nds_usl_data, insert_into.format(vhod_nds_usl_data['table_name'], vhod_nds_usl_data['insert_values']))
    update_from_dbf(create_tranformed_list(create_list_base_tables()[6], t493_tn_nds_tables)[list_number], select_all.format(vhod_nds_tn_data['table_name']), base_number, vhod_nds_tn_data, insert_into.format(vhod_nds_tn_data['table_name'], vhod_nds_tn_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[7], incoming_tovary_tables) [list_number], select_all.format(nds_tovary_data['table_name']), base_number, nds_tovary_data, insert_into.format(nds_tovary_data['table_name'], nds_tovary_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[9], currency_tables)[list_number], select_all.format(currency_data['table_name']), base_number, currency_data, insert_into.format(currency_data['table_name'], currency_data['insert_values']))

    update_from_dbf(create_tranformed_list(create_list_base_tables()[8], countries_tables)[list_number], select_all.format(countries_data['table_name']), base_number, countries_data, insert_into.format(countries_data['table_name'], countries_data['insert_values']))


    pass
