#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 

tn_providers =  "contragents_documents.doc_type != '0'"
pp_providers =  "contragents_documents.doc_type = '0'"

tn_buyers = "contragents_documents_two.doc_type = '0' "
pp_buyers = "contragents_documents_two.doc_type != '0'"

select_all_documents="SELECT * FROM contragents_documents;"
select_contragents_identificator = "SELECT id FROM contragents;"
select_id_docs = "SELECT parent FROM contragents_documents;"

select_docs = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {} 
ORDER BY contragents_documents.doc_date;
"""



#ACT SVERKI\HVOSTY
select_docs_poluchenoe = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {} 
ORDER BY contragents_documents.doc_date;
"""

select_docs_prodanoe = """
SELECT * FROM contragents_documents_two
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id 
WHERE {} AND contragents_documents_two.parent = {} 
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
WHERE {} AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents_two.doc_date;
"""
