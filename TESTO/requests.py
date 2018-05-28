#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 


income_tn_nds = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents.id=contragents_documents_two.parent
LEFT JOIN vhod_nds_tn ON vhod_nds_tn.full_sum=contragents_documents_two.summ
AND contragents_documents_two.doc_date=vhod_nds_tn.data
WHERE contragents_documents_two.doc_date >= '2018-01-01'
AND contragents_documents_two.doc_date <= '2018-03-31'
AND contragents_documents_two.deleted !='*'
AND contragents_documents_two.currency_type = '1'
AND contragents_documents_two.provider_account_type != '3649U'
AND contragents_documents_two.doc_type ='0';
"""



income_serv_nds = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents.id=contragents_documents_two.parent
LEFT JOIN vhod_nds_usl ON vhod_nds_usl.full_sum=contragents_documents_two.summ
AND contragents_documents_two.doc_date=vhod_nds_usl.data
WHERE contragents_documents_two.doc_date >= '2018-01-01'
AND contragents_documents_two.doc_date <= '2018-03-31'
AND contragents_documents_two.deleted !='*'
AND contragents_documents_two.currency_type = '1'
AND contragents_documents_two.provider_account_type != '3649U'
AND contragents_documents_two.doc_type ='0';
"""



income_tovary = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents.id=contragents_documents_two.parent
LEFT JOIN nds_tovary ON nds_tovary.full_sum=contragents_documents_two.summ
AND contragents_documents_two.doc_date=nds_tovary.data
WHERE contragents_documents_two.doc_date >= '2018-01-01'
AND contragents_documents_two.doc_date <= '2018-03-31'
AND contragents_documents_two.deleted !='*'
AND contragents_documents_two.currency_type = '1'
AND contragents_documents_two.provider_account_type != '3649U'
AND contragents_documents_two.doc_type ='0';
"""



outcome_tn_nds = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents.id=contragents_documents.parent
LEFT JOIN ishod_nds_tn ON ishod_nds_tn.full_sum=contragents_documents.summ
AND contragents_documents.doc_date=ishod_nds_tn.data
WHERE contragents_documents.doc_date >= '2018-01-01'
AND contragents_documents.doc_date <= '2018-03-31'
AND contragents_documents.deleted !='*'
AND contragents_documents.back_flag ='0'
AND contragents_documents.pay_type != '2MS'
AND contragents_documents.doc_type !='0';
"""


outcome_serv_nds = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents.id=contragents_documents.parent
LEFT JOIN ishod_nds_usl ON ishod_nds_usl.full_sum=contragents_documents.summ
AND contragents_documents.doc_date=ishod_nds_usl.data
WHERE contragents_documents.doc_date >= '2018-01-01'
AND contragents_documents.doc_date <= '2018-03-31'
AND contragents_documents.deleted !='*'
AND contragents_documents.back_flag ='0'
AND contragents_documents.pay_type != '2MS'
AND contragents_documents.doc_type !='0';
"""



#---------------------------------------------------------------


courses_colls = '(data, name, scale, rate)'
insert_courses = "INSERT INTO {} VALUES (?,?,?,?);"

select_usd_course = "SELECT * FROM usd WHERE data >= {} AND  data <= {};"
select_eur_course = "SELECT * FROM eur WHERE data >= {} AND  data <= {};"
select_grivn_course = "SELECT * FROM grivna WHERE data >= {} AND  data <= {};"
select_rus_course = "SELECT * FROM rus WHERE data >= {} AND  data <= {};"


select_curr_income =  """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id
LEFT JOIN countries   ON contragents.country =countries.dbf_id
WHERE contragents_documents_two.doc_date >= {} 
AND contragents_documents_two.doc_date <= {}
AND contragents_documents_two.deleted != '*'
AND contragents_documents_two.doc_type = '0'
AND contragents_documents_two.currency_type != '1'
ORDER BY contragents_documents_two.doc_date;
"""  



select_curr_outcome =  """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id
LEFT JOIN countries   ON contragents.country =countries.dbf_id
WHERE contragents_documents.doc_date >= {} 
AND contragents_documents.doc_date <= {}
AND contragents_documents.deleted != '*'
AND contragents_documents.doc_type != '0'
AND contragents_documents.currency_type != '1'
ORDER BY contragents_documents.doc_date;
"""  
