
import os


#625 - накладные отправленные и платежки за них
#493 - материалы пришедшие и платежи от нас

not_del = "contragents_documents.deleted != '*'"


start_data = "2014-06-30"
ending_data = "2017-11-10"


tn_providers =  "contragents_documents.doc_type != '0'"
pp_providers =  "contragents_documents.doc_type = '0'"


tn_buyers = "contragents_documents_two.doc_type = '0'"
pp_buyers = "contragents_documents_two.doc_type != '0'"


select_contragents_identificator = "SELECT id FROM contragents WHERE deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents WHERE deleted != '*';"

select_docs_poluchenoe = """
SELECT * FROM contragents_documents 
LEFT JOIN contragents ON contragents_documents.parent=contragents.id 
WHERE {} AND contragents_documents.parent = {} 
AND  doc_date >= {} 
AND  doc_date <= {} 
AND contragents_documents.deleted != '*'
ORDER BY contragents_documents.doc_date;
"""

select_docs_prodanoe = """
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
