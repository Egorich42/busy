#! /usr/bin/env python
# -*- coding: utf-8 -*

from datetime import *

today = date.today()
this_year = date.today().year
this_month = date.today().month

first_kvartal_end = date(this_year, 3,31)
second_kvartal_end= date(this_year,6,30)
third_kvartal_end= date(this_year,9,30)
four_kvartal_end = date(this_year,12,31)


first_kvartal_start = date(this_year, 1,1)
second_kvartal_start= date(this_year,4,1)
third_kvartal_start= date(this_year,7,1)
four_kvartal_start = date(this_year,10,1)

taxes = (('USN', 'usn.'),('NDS', 'nds.'),)

def current_kvartal():
    if today<first_kvartal_end:
        cur_kvart = first_kvartal_start
    if today > first_kvartal_end and today < second_kvartal_end:
        cur_kvart = second_kvartal_start
    if today >third_kvartal_start and today <third_kvartal_end:
        cur_kvart = third_kvartal_start
    if today > four_kvartal_start and today < four_kvartal_end:
        cur_kvart = four_kvartal_start    
        pass
    return cur_kvart
    pass



def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 

bazi = ('dipartD', 'avangard', 'ditest','ipmatusev','mitada', 'smdpark','himprom_den', 'polymia_den')
location ='D:\DATA_SETS' 
t625 = location+'\{}\SC625.DBF'
t625_tables_names = ('DESCR','PARENTEXT','ISMARK','SP609', 'SP611','SP613', 'SP617','VERSTAMP','SP615','SP619', 'SP623','SP620')

t493 = location+'\{}\SC493.DBF'
t493_tables_names = ('DESCR','PARENTEXT','ISMARK', 'SP467', 'SP468','SP470','SP482','VERSTAMP','SP482','SP480','SP479','SP478')

t167 = location+'\{}\SC167.DBF'
t167_tables = ('ID','DESCR', 'ISMARK','SP134', 'SP137')

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