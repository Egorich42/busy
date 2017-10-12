import sqlite3

conn = sqlite3.connect('1.sqlite')
cur = conn.cursor()

contragent_id = 17
pp ="contragents_documents.summm != '0'"
tn = "contragents_documents.summm = '0'"
start_date = "'2016-09-02'"
end_date = "'2016-09-12'"

select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
  
#select_tn = select_docs.format(tn, contragent_id, ind)   
select_pp = select_docs.format(pp, contragent_id, start_date, end_date)



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

print(all_pp)