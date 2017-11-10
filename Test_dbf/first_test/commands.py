
import os

tn =  "contragents_documents.doc_type != '0'"
pp =  "contragents_documents.doc_type = '0'"


tn_providers = "contragents_documents_two.doc_type = '0'"
pp_providers = "contragents_documents_two.doc_type != '0'"

start_data = "2017-09-01"
ending_data = "2017-11-11"

select_contragents_identificator = "SELECT id FROM contragents WHERE deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents WHERE deleted != '*';"

select_docs_buyers = """
SELECT * FROM contragents_documents 
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {} 
AND contragents_documents.deleted != '*'
ORDER BY contragents_documents.doc_date;
"""

select_docs_providers = """
SELECT * FROM contragents_documents_two 
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id 
WHERE {} 
AND contragents_documents_two.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {}
AND contragents_documents_two.deleted != '*' 
ORDER BY contragents_documents_two.doc_date;
"""

select_docs_to = """
SELECT * FROM contragents_documents 
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
AND contragents_documents.deleted != '*' 
ORDER BY contragents_documents.doc_date;
"""
select_docs_from = """
SELECT * FROM contragents_documents_two 
LEFT JOIN contragents ON contragents_documents_two.parent=contragents.id 
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
AND contragents_documents_two.deleted != '*' 
ORDER BY contragents_documents_two.doc_date;
"""
