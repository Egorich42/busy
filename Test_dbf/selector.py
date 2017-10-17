import sqlite3
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools

conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

contragent_id = 17
tn ="contragents_documents.summm != '0'"
pp = "contragents_documents.summm = '0'"
start_date = "'2016-01-01'"
end_date = "'2016-09-12'"

#select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
  
#select_tn = select_docs.format(tn, contragent_id, ind)   
#select_pp = select_docs.format(pp, contragent_id, start_date, end_date)

select_pp = select_docs.format(pp, start_date, end_date)
select_tn = select_docs.format(tn, start_date, end_date)   


def create_list_of_table_values(request_text):
    request_name = cur.execute(request_text).fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in cur.description]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass    


all_pp = create_list_of_table_values(select_pp)
all_tn = create_list_of_table_values(select_tn)


sorted_pp = sorted(all_pp, key=lambda item: item['id'])
sorted_tn = sorted(all_tn, key=lambda item: item['id'])


def perebor(data_sorted, one, two,  three):
	beta = []
	albert = []
	for key, group in itertools.groupby(data_sorted, key=lambda x:x[one]):
		a = list(sorted(group, key=lambda item: item[two]))
		albert += [sum([f[key] for key in[three] for f in a])]
		beta += [s for s in a]
		print(a[0]['contragent_name'])
	return (albert, beta)



nn = perebor(sorted_tn, 'id', 'doc_date',  'summ')
mm = perebor(sorted_pp, 'id', 'doc_date', 'summ')
rt = perebor(sorted_pp, 'contragent_name', 'doc_date', 'summ')
