import sqlite3
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools

conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

contragent_id = "'17'"
tn ="contragents_documents.doc_type != '0'"
pp = "contragents_documents.doc_type = '0'"
start_date = "'2015-01-01'"
end_date = "'2018-09-12'"
all_acts = "contragents_documents.doc_type = '0' OR '2MX' OR '2N2'"

select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
#select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_contragents_identificator = "SELECT id FROM contragents;"
select_id_docs = "SELECT parent FROM contragents_documents;"
  



def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 
 
def get_pays_balance(pp_list, tn_list, element_name):
    pp_suma = sum(float(res[element_name]) for res in pp_list)
    tn_suma = sum(float(res[element_name]) for res in tn_list)

    if pp_suma < tn_suma:
        resultat = 'сумма задолженности контрагента составляет'+' '+str(tn_suma-pp_suma)
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'+' '+str(pp_suma-tn_suma)
    if pp_suma == tn_suma:
        resultat = 'OK!'
    return resultat
    pass   

select_tn = select_docs.format(tn, str(contragent_id), start_date,end_date)
select_pp = select_docs.format(pp, str(contragent_id), start_date, end_date)
#print(select_tn)
all_pp = create_list_of_table_values(cur.execute(select_pp),cur.description)
all_tn = create_list_of_table_values(cur.execute(select_tn),cur.description)
#print(all_tn)
summa_sverki = get_pays_balance(all_pp, all_tn, 'summ')
contr_name = all_tn[0]['full_name']
#print(summa_sverki)
#print(contr_name)



gg_hf = create_list_of_table_values(cur.execute(select_contragents_identificator),cur.description)
#mrt = create_list_of_table_values(cur.execute(select_id_docs),cur.description)


archi = [nrm['id'] for nrm in gg_hf]
print(archi)
for altair in archi[5:9]:
    select_tn2 = select_docs.format(tn, "'"+str(altair)+"'", start_date,end_date)
    select_pp2 = select_docs.format(pp, "'"+str(altair)+"'", start_date, end_date)
    all_pp2 = create_list_of_table_values(cur.execute(select_pp2),cur.description)
    all_tn2 = create_list_of_table_values(cur.execute(select_tn2),cur.description)
    summa_sverki = get_pays_balance(all_pp2, all_tn2, 'summ')

    if summa_sverki !='OK!' and len(all_tn2)>0:
        all_tn2[0]['name']+" "+summa_sverki
        pass


                  
#summa_sverki = get_pays_balance(all_pp, all_tn, 'summ')

#contr_name = all_tn[0]['full_name']
#sorted_pp = sorted(all_pp, key=lambda item: item['id'])
#sorted_tn = sorted(all_tn, key=lambda item: item['id'])


#M 1K
