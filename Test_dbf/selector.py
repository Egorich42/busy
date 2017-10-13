import sqlite3
from itertools import groupby
import collections
from collections import defaultdict
conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

contragent_id = 17
pp ="contragents_documents.summm != '0'"
tn = "contragents_documents.summm = '0'"
start_date = "'2016-01-01'"
end_date = "'2016-09-12'"

#select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
  
#select_tn = select_docs.format(tn, contragent_id, ind)   
#select_pp = select_docs.format(pp, contragent_id, start_date, end_date)

select_pp = select_docs.format(pp, start_date, end_date)


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
#all_tn = create_list_of_table_values(select_tn)

#print(all_pp[2:6])

#my_list = [{'name':'Homer', 'age':39}, {'name':'Bart', 'age':10}]

my_list = sorted(all_pp[:10], key=lambda k: k['contragent_name'])

#persons = [{'person':'guybrush','job':'pirate'},{'person':'leChuck','job':'pirate'}, {'person':'elaine','job':'governor'}]
persons = my_list
persons_by_jobs = defaultdict(list)
for person in persons:
    persons_by_jobs[person['id']].append(person['summ'])
print(persons_by_jobs)    

a=[]
for i in persons_by_jobs[1]:
	print(sum(i))


