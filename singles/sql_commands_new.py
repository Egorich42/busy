#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 



pp_providers_model =  """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.act_detector = '2' 
AND {}
"""
pp_providers_standart_id = "contragents_documents.pay_identif = '2MP'"
pp_providers_cashback_id = "contragents_documents.pay_identif = '2MS' "
pp_providers_dpd_id = "AND contragents_documents.pay_identif != 'S5C' "


tn_providers =  "contragents_documents.doc_type != '0' AND contragents_documents.deleted !='*'"
tn_providers_no_del = "contragents_documents.doc_type != '0' AND contragents_documents.test_del == '10'"



pp_providers = pp_providers_model.format(pp_providers_standart_id)
pp_providers_vozvr = pp_providers_model.format(pp_providers_cashback_id)
pp_providers_dpd  = pp_providers_model.format(pp_providers_dpd_id)


tn_providers =  "contragents_documents.doc_type != '0' AND contragents_documents.deleted !='*'"
tn_providers_no_del = "contragents_documents.doc_type != '0' AND contragents_documents.test_del == '10'"


tn_buyers = "contragents_documents_two.doc_type = '0' AND contragents_documents_two.deleted !='*'"

pp_buyers = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector !='S5B' AND contragents_documents_two.pp_detector !='2MM'"
pp_buyers_vozvr = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector =='S5B'"
pp_buyers_dpd = "contragents_documents_two.doc_type != '0' AND contragents_documents_two.deleted !='*' AND contragents_documents_two.pp_detector =='2MM'"



#contragents_documents:

#---------------PROVIDERS:
prov_dpd
НАКЛАДНЫЕ/АКТЫ:
	tn_providers =  "contragents_documents.doc_type != '0' AND contragents_documents.deleted !='*'"
	tn_providers_no_del = "contragents_documents.doc_type != '0' AND contragents_documents.test_del == '10'"

АКТ:
	doc_type = 2MX 

Акт конт обмер: и просо акты (УО СПОРТА И ТУРИЗМА, в ДИТЭСТЕ):
	doc_type = 2N0 (Хрен знает, что это вообще такое)

Хз. что за кат: 
	doc_type = QXY 

ТТН:
	doc_type =  2MW 

test_del:
	1 - удалена к чертям
	0 - черт его знает
	N -  черт его знает
	10 - удалена-но-не-удалена

по идентификатору:
pay_identif = 0

#----------------Платежи (ПП)

pp_providers_model =  """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.act_detector = '2' 
AND {}
"""
pp_providers_standart_id = "contragents_documents.pay_identif = '2MP'"
pp_providers_cashback_id = "contragents_documents.pay_identif = '2MS' "
pp_providers_dpd_id = "AND contragents_documents.pay_identif != 'S5C' "


pp_providers = pp_providers_model.format(pp_providers_standart_id)
pp_providers_cashback = pp_providers_model.format(pp_providers_cashback_id)
pp_providers_dpd  = pp_providers_model.format(pp_providers_dpd_id)

#-----------------------#
станадртный ПП, иногда - Счет: doc_type = 0, 
	act_detector = 2
	pay_identif = 2MP


Платежка, возврат от поставщиков:
	 pay_identif = S5C

Договор перевода долга:
	pay_identif = 2MS

Возвратная наклдная//акт, сумма с минусом:
	col_side_id = 1

Хрен знает, что это, Райтрейд(ПП 1322 от 31.12.13 г.,  в ДИТЭСТЕ) = pay_identif = 2MQ


#-------------BUYERS: