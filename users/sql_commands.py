#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 

tn_providers =  "contragents_documents.doc_type != '0' AND contragents_documents.deleted !='*'"
tn_providers_no_del = "contragents_documents.doc_type != '0' AND contragents_documents.test_del == '10'"

pp_providers =  "contragents_documents.doc_type = '0' AND contragents_documents.deleted !='*' AND contragents_documents.act_detector != '3' AND contragents_documents.pay_identif != 'S5C'"
pp_providers_vozvr = "contragents_documents.doc_type = '0' AND contragents_documents.deleted !='*' AND contragents_documents.pay_identif == 'S5C'"


tn_buyers = "contragents_documents_two.doc_type = '0' AND contragents_documents_two.deleted !='*'"
pp_buyers = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector !='S5B' AND contragents_documents_two.pp_detector !='2MM'"

pp_buyers_vozvr = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector =='S5B'"
pp_buyers_dpd = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector =='2MM'"




select_contragents = "SELECT * FROM contragents;"
select_all_documents="SELECT * FROM contragents_documents;"
select_all_documents_two="SELECT * FROM contragents_documents_two;"

select_contragents_identificator = "SELECT id FROM contragents WHERE contragents.deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents;"
select_contragent_name ="SELECT name FROM contragents WHERE id = {};"

insert_into_docs ="INSERT INTO contragents_documents VALUES (?,?,?,?,?,?,?,?,?,?);"
insert_into_docs_two ="INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?,?,?,?,?);"
insert_into_contragents ="INSERT INTO contragents VALUES (?,?,?,?,?);"


select_every_docs = """
SELECT * FROM contragents_documents
LEFT JOIN contragents_documents_two
WHERE contragents_documents.doc_type = '0' AND contragents_documents.deleted !='*'
AND contragents_documents.doc_type != '0' AND contragents_documents.test_del == '10'
AND contragents_documents_two.doc_type = '0' AND contragents_documents_two.deleted !='*'
ORDER BY contragents_documents.doc_date
AND contragents_documents_two.doc_date;
"""


select_contragents_identificator = "SELECT id FROM contragents WHERE contragents.deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents;"
select_contragent_name ="SELECT name FROM contragents WHERE id = {};"

docs_on_main = """
SELECT * FROM {}
WHERE {}
ORDER BY doc_date;
"""

select_docs = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {}

ORDER BY contragents_documents.doc_date;
"""



#ACT SVERKI\HVOSTY
select_documents_from_providers = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {}  
AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents.doc_date;
"""


select_documents_to_buyers = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id 
WHERE {} 
AND contragents_documents_two.parent = {}
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents_two.doc_date;
"""


#CUR_FIN_STATE
select_docs_to_buyers =  """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {} 
ORDER BY contragents_documents.doc_date;
"""

select_docs_from_providers = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id 
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents_two.doc_date;
"""
