#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 


tn_providers =  """
contragents_documents.doc_type != '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.pay_type != '2MS'
AND contragents_documents.back_flag != 1
"""

tn_providers_no_del = """
contragents_documents.doc_type != '0' 
AND contragents_documents.del_counter == '10'
"""

tn_providers_moneyback =  """
contragents_documents.doc_type != '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.back_flag = 1
"""

pp_providers =  """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*' 
AND contragents_documents.operation_type != '3' 
AND contragents_documents.pay_type != 'S5C'
"""

pp_providers_vozvr = """
contragents_documents.doc_type = '0' 
AND contragents_documents.deleted !='*'
AND contragents_documents.pay_type == 'S5C'
"""


tn_buyers = """
contragents_documents_two.doc_type = '0' 
AND contragents_documents_two.deleted !='*'
AND contragents_documents_two.provider_account_type != '3649U'
"""

pp_buyers = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pay_type !='S5B' 
AND contragents_documents_two.pay_type !='2MM'
AND contragents_documents_two.currency_type !='2'
"""

pp_buyers_vozvr = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pay_type =='S5B'
"""

pp_buyers_dpd = """
contragents_documents_two.doc_type != '0' 
AND contragents_documents_two.deleted !='*' 
AND contragents_documents_two.pay_type =='2MM'
"""
docs_on_main = "SELECT * FROM {} WHERE {} ORDER BY doc_date DESC;"



