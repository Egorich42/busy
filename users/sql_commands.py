#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 


tn_providers =  """
contragents_documents.doc_type != '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.pay_identif != '2MS'
AND contragents_documents.col_side_id != 1
"""

tn_providers_no_del = """
contragents_documents.doc_type != '0' 
AND contragents_documents.test_del == '10'
"""

tn_providers_moneyback =  """
contragents_documents.doc_type != '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.col_side_id = 1
"""

pp_providers =  """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.act_detector != '3' 
AND contragents_documents.pay_identif != 'S5C'
"""

pp_providers_vozvr = """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*'
AND contragents_documents.pay_identif == 'S5C'
"""


tn_buyers = """
contragents_documents_two.doc_type = '0' 
AND contragents_documents_two.deleted !='*'
AND contragents_documents_two.type_sort != '3649U'
"""

pp_buyers = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pp_detector !='S5B' 
AND contragents_documents_two.pp_detector !='2MM'
AND contragents_documents_two.another_identif !='2'
"""

pp_buyers_vozvr = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pp_detector =='S5B'
"""

pp_buyers_dpd = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pp_detector =='2MM'
"""

def sel_all(name):
	sel = "SELECT * FROM {};".format(name)
	return sel
	pass


def sel_to_hvosty(table_name):
	command  =	"""
	SELECT * FROM table_name
	LEFT JOIN contragents ON table_name.parent=contragents.id 
	WHERE {}  
	AND table_name.parent = {} 
	AND  doc_date >= {} 
	AND  doc_date <= {}
	ORDER BY table_name.doc_date;
	""".replace("table_name", table_name)
	return command 
	pass


def sel_to_cur_fin(table_name):
	command = """
	SELECT * FROM table_name
	LEFT JOIN contragents ON table_name.parent=contragents.id 
	WHERE {} 
	AND  doc_date >= {} 
	AND  doc_date <= {}
	ORDER BY table_name.doc_date;
	""".replace("table_name", table_name)
	return command 
	pass


def sel_to_cur_fin_state_with_nds(main_table_name, nds_table_tn, nds_table_usl):
	command = """
	SELECT * FROM main_table_name
	LEFT JOIN contragents ON main_table_name.parent=contragents.id
	LEFT JOIN nds_table_tn ON main_table_name.summ=nds_table_tn.full_sum
	AND main_table_name.doc_date=nds_table_tn.data
	LEFT JOIN nds_table_usl ON main_table_name.summ=nds_table_usl.full_sum
	AND main_table_name.doc_date=nds_table_usl.data

	WHERE {} 
	AND  doc_date >= {} 
	AND  doc_date <= {}
	ORDER BY main_table_name.doc_date;
	"""
	return command
	pass

"""
select_contragents = sel_all("contragents;")
select_all_documents=sel_all("contragents_documents;")
select_all_documents_two=sel_all("contragents_documents_two;")
select_all_eschf_outer=sel_all("eschf_outer;")

select_all_ishod_nds_tn=sel_all("ishod_nds_tn;")
select_all_ishod_nds_usl=sel_all("ishod_nds_usl;")

select_all_vhod_nds_tn=sel_all("vhod_nds_tn;")
select_all_vhod_nds_usl=sel_all("vhod_nds_usl;")
"""

select_contragents = "SELECT * FROM contragents;"
select_all_documents="SELECT * FROM contragents_documents;"
select_all_documents_two="SELECT * FROM contragents_documents_two;"
select_all_eschf_outer="SELECT * FROM eschf_outer;"

select_all_ishod_nds_tn="SELECT * FROM ishod_nds_tn;"
select_all_ishod_nds_usl="SELECT * FROM ishod_nds_usl;"
select_all_vhod_nds_tn="SELECT * FROM vhod_nds_tn;"
select_all_vhod_nds_usl="SELECT * FROM vhod_nds_usl;"



select_contragents_identificator = "SELECT id FROM contragents WHERE contragents.deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents;"
select_contragent_name ="SELECT name FROM contragents WHERE id = {};"


insert_into_docs ="INSERT INTO contragents_documents VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
insert_into_docs_two ="INSERT INTO contragents_documents_two VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
insert_into_contragents ="INSERT INTO contragents VALUES (?,?,?,?,?);"
insert_into_eschf_outer ="INSERT INTO eschf_out VALUES (?,?,?,?,?);"

insert_usl_okaz_nds ="INSERT INTO ishod_nds_usl VALUES (?,?,?,?,?);"
insert_tn_otpravl_nds="INSERT INTO ishod_nds_tn VALUES (?,?,?,?,?);"

insert_usl_poluch_nds ="INSERT INTO vhod_nds_usl VALUES (?,?,?,?,?);"
insert_tn_vhod_nds="INSERT INTO vhod_nds_tn VALUES (?,?,?,?,?);"


select_contragents_identificator = "SELECT id FROM contragents WHERE contragents.deleted != '*';"
select_id_docs = "SELECT parent FROM contragents_documents;"
select_contragent_name ="SELECT name FROM contragents WHERE id = {};"

docs_on_main = """
SELECT * FROM {}
WHERE {}
ORDER BY doc_date;
"""

#ACT SVERKI\HVOSTY
select_documents_from_providers = sel_to_hvosty('contragents_documents')
select_documents_to_buyers = sel_to_hvosty('contragents_documents_two')

#CUR_FIN_STATE
select_docs_to_buyers = sel_to_cur_fin('contragents_documents')
select_docs_from_providers = sel_to_cur_fin('contragents_documents_two')


#_____________________________________________________________#

sel_docs_with_ishod_nds = """
SELECT * FROM contragents_documents
LEFT JOIN contragents ON contragents_documents.parent=contragents.id
LEFT JOIN ishod_nds_usl ON contragents_documents.summ=ishod_nds_usl.full_sum
AND contragents_documents.doc_date=ishod_nds_usl.data
LEFT JOIN ishod_nds_tn ON contragents_documents.summ=ishod_nds_tn.full_sum
AND contragents_documents.doc_date=ishod_nds_tn.data

WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents.doc_date;
"""

sel_vhod_tn_nds = """
SELECT contragents_documents_two.document_name, 
contragents_documents_two.contragent_name, 
contragents_documents_two.doc_date, 
contragents_documents_two.summ, 
contragents_documents_two.parent,
vhod_nds_tn.full_sum,
vhod_nds_tn.nds,
vhod_nds_tn.bez_nds
FROM contragents_documents_two
INNER JOIN contragents ON contragents.id = contragents_documents_two.parent
INNER JOIN vhod_nds_tn ON vhod_nds_tn.full_sum = contragents_documents_two.summ
AND contragents_documents_two.doc_date=vhod_nds_tn.data
AND contragents_documents_two.parent=vhod_nds_tn.parent
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents_two.doc_date;
"""



sel_vhod_usl_nds = """
SELECT contragents_documents_two.document_name, 
contragents_documents_two.contragent_name, 
contragents_documents_two.doc_date, 
contragents_documents_two.summ, 
contragents_documents_two.parent,
vhod_nds_usl.full_sum,
vhod_nds_usl.nds,
vhod_nds_usl.bez_nds
FROM contragents_documents_two
INNER JOIN contragents ON contragents.id = contragents_documents_two.parent
INNER JOIN vhod_nds_usl ON vhod_nds_usl.full_sum = contragents_documents_two.summ
AND contragents_documents_two.doc_date=vhod_nds_usl.data
AND contragents_documents_two.parent=vhod_nds_usl.parent
WHERE {} 
AND  doc_date >= {} 
AND  doc_date <= {}
ORDER BY contragents_documents_two.doc_date;
"""


#_____________________________________________________________#

select_eschf_documents= """
SELECT * FROM outer_eschf
LEFT JOIN contragents ON outer_eschf.parent=contragents.id 
WHERE  doc_data >= {} 
AND  doc_data <= {}
ORDER BY outer_eschf.doc_data;
"""