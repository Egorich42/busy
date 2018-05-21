from django.db import models
import sqlite3 
from dbfread import DBF
import os.path


select_contragents = "SELECT * FROM contragents;"

select_all_documents="SELECT * FROM contragents_documents;"
select_all_documents_two="SELECT * FROM contragents_documents_two;"


sel_ishod_nds_tn="SELECT * FROM ishod_nds_tn;"
sel_ishod_nds_usl="SELECT * FROM ishod_nds_usl;"

sel_vhod_tn_nds="SELECT * FROM vhod_nds_tn;"
sel_vhod_usl_nds="SELECT * FROM vhod_nds_usl;"

select_all_tovary="SELECT * FROM nds_tovary;"

select_countries="SELECT * FROM countries;"
select_currency="SELECT * FROM currency;"


insert_into_docs = "INSERT INTO contragents_documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
insert_into_docs_two = "INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"


insert_into_contragents = "INSERT INTO contragents VALUES (?,?,?,?,?,?);"
insert_into_eschf_outer = "INSERT INTO eschf_out VALUES (?,?,?,?,?);"

insert_usl_okaz_nds = "INSERT INTO ishod_nds_usl VALUES (?,?,?,?,?);"
insert_tn_otpravl_nds= "INSERT INTO ishod_nds_tn VALUES (?,?,?,?,?);"

insert_usl_poluch_nds = "INSERT INTO vhod_nds_usl VALUES (?,?,?,?,?);"
insert_tn_vhod_nds= "INSERT INTO vhod_nds_tn VALUES (?,?,?,?,?);"

insert_tovary = "INSERT INTO nds_tovary VALUES (?,?,?,?,?);"


insert_countries = "INSERT INTO countries VALUES (?,?,?,?,?);"
insert_currency = "INSERT INTO currency  VALUES (?,?,?,?);"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


f = open(BASE_DIR+'\\'+'bases.txt')
bazi = [line.split(',') for line in f][0]



location = BASE_DIR
t625 = location+'\{}\SC625.DBF'
t625_tables_names = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP620')

t493 = location+'\{}\SC493.DBF'
t493_tables_names = ('DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480','SP479','SP478')

t167 = location+'\{}\SC167.DBF'
t167_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137', 'SP155')

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


countries = location+'\{}\SC576.DBF'
countries_tables = ('ID','CODE','DESCR','SP574','SP33760')


currency = location+'\{}\SC114.DBF'
currency_tables = ('ID', 'CODE','DESCR','SP105')


contragents_colls = '(id, name, deleted, full_name, unp, country)'
contragents_docs_colls = '(document_name, parent, deleted, contragent_name, doc_date,summ, doc_type, test_del, act_detector, pay_identif, col_side_id, type_sort)'
contragents_docs_two_colls = '(document_name, parent, deleted, contragent_name, doc_date, summ, doc_type, test_del, pp_detector, currency_type, another_id, type_sort)'
nds_docs_colls = '(parent, data, full_sum, nds, bez_nds)'

countries_colls = '(dbf_id, code, name, country_type, ts_marker)'
currency_colls = '(dbf_id, code, name, currency_id)'


contragents_data = {'table_name': 'contragents', 'coll_names':contragents_colls}
contragents_docs_data = {'table_name':  'contragents_documents', 'coll_names':contragents_docs_colls  }
contragents_docs_two_data = {'table_name':  'contragents_documents_two', 'coll_names':contragents_docs_two_colls  }
ishod_nds_tn_data = {'table_name':'ishod_nds_tn', 'coll_names':nds_docs_colls }
ishod_nds_usl_data = {'table_name':'ishod_nds_usl', 'coll_names':nds_docs_colls }
nds_tovary_data = {'table_name':'nds_tovary', 'coll_names':nds_docs_colls }
vhod_nds_tn_data = {'table_name':'vhod_nds_tn', 'coll_names':nds_docs_colls }
vhod_nds_usl_data = {'table_name':'vhod_nds_usl', 'coll_names':nds_docs_colls }

countries_data = {'table_name': 'countries', 'coll_names': countries_colls }
currency_data = {'table_name': 'currency',  'coll_names': currency_colls }



def get_data_from_dbf(table_name):
    dataset = list(DBF(table_name, encoding='iso-8859-1'))
    return dataset
    pass


def get_docs_with_nds(from_dbf_table, tables_names):
    values_list = []
    for i in from_dbf_table:    
        values_list += [(
                        str(dict(i)[tables_names[0]]).replace(" ", ""),
                        dict(i)[tables_names[1]],
                        dict(i)[tables_names[2]],
                        dict(i)[tables_names[3]],
                        dict(i)[tables_names[4]]
                        )]
    return values_list  
    pass






def get_countries(from_dbf_table, tables_names):
    values_list = []
    for i in from_dbf_table:    
        values_list += [(dict(i)[tables_names[0]],
                        dict(i)[tables_names[1]],
                        str(dict(i)[tables_names[2]]).replace(" ", ""),
                        dict(i)[tables_names[3]],
                        dict(i)[tables_names[4]])]
    return values_list  
    pass








def get_currency(from_dbf_table, tables_names):
    values_list = []
    for i in from_dbf_table:    
        values_list += [(dict(i)[tables_names[0]],
                        dict(i)[tables_names[1]],
                        str(dict(i)[tables_names[2]]).replace(" ", ""),
                        dict(i)[tables_names[3]])]
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
                        dict(i)[tables_names[4]].replace(" ", ""),
                        dict(i)[tables_names[5]].replace(" ", "")
                        )]                      
    return values_list  
    pass


def contragents_list(numar,table_names):
    dot = range(len(bazi))
    fiat = []
    for t in dot:
        documents_table = [get_data_mudaki(numar[t], table_names)]
        fiat += [ti for ti in documents_table]
    return fiat 
    pass


def create_list_base_tables():
    big_tables_list = []
    for x in (t625,t493, t167, t625_uslugi_nds, t625_tn_nds, t493_uslugi_nds, t493_tn_nds, incoming_tovary_nds, countries, currency):
        tables_in_bases = [get_data_from_dbf(x.format(i)) for i in bazi]

        big_tables_list +=[tables_in_bases]
    return  big_tables_list
    pass


def create_lists_with_nds(numar, table_names):
    fiat = []
    for t in range(len(bazi)):
        documents_table = [get_docs_with_nds(numar[t], table_names)]
        fiat += [ti for ti in documents_table]
    return fiat 
    pass




def create_countries_list(numar, table_names):
    fiat = []
    for t in range(len(bazi)):
        documents_table = [get_countries(numar[t], table_names)]
        fiat += [ti for ti in documents_table]
    return fiat 
    pass


def create_currency_list(numar, table_names):
    fiat = []
    for t in range(len(bazi)):
        documents_table = [get_currency(numar[t], table_names)]
        fiat += [ti for ti in documents_table]
    return fiat 
    pass




def create_lists_without_nds(numar, table_names):
    fiat = []
    for t in range(len(bazi)):
        documents_table = [get_data(numar[t], table_names)]
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
    update_from_dbf(contragents_list(create_list_base_tables()[2],t167_tables)[list_number], select_contragents, base_number, contragents_data, insert_into_contragents)

    update_from_dbf(create_lists_without_nds(create_list_base_tables()[0],t625_tables_names)[list_number], select_all_documents, base_number, contragents_docs_data, insert_into_docs)
    update_from_dbf(create_lists_without_nds(create_list_base_tables()[1],t493_tables_names)[list_number], select_all_documents_two, base_number, contragents_docs_two_data, insert_into_docs_two)

    update_from_dbf(create_lists_with_nds(create_list_base_tables()[3], t625_uslugi_nds_tables )[list_number], sel_ishod_nds_usl, base_number, ishod_nds_usl_data, insert_usl_okaz_nds)
    update_from_dbf(create_lists_with_nds(create_list_base_tables()[4], t625_tn_nds_tables )[list_number], sel_ishod_nds_tn, base_number, ishod_nds_tn_data, insert_tn_otpravl_nds)

    update_from_dbf(create_lists_with_nds(create_list_base_tables()[5], t493_uslugi_nds_tables)[list_number], sel_vhod_usl_nds, base_number, vhod_nds_usl_data, insert_usl_poluch_nds)
    update_from_dbf(create_lists_with_nds(create_list_base_tables()[6], t493_tn_nds_tables)[list_number], sel_vhod_tn_nds, base_number, vhod_nds_tn_data, insert_tn_vhod_nds)

    update_from_dbf(create_lists_with_nds(create_list_base_tables()[7], incoming_tovary_tables) [list_number], select_all_tovary, base_number, nds_tovary_data, insert_tovary)
    
    update_from_dbf(create_currency_list(create_list_base_tables()[9], currency_tables)[list_number], select_currency, base_number, currency_data, insert_currency)
    update_from_dbf(create_countries_list(create_list_base_tables()[8], countries_tables)[list_number], select_countries, base_number, countries_data, insert_countries)

    pass
