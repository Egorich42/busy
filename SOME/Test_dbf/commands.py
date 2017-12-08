
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




def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 


def perebor(data_sorted, one, two, three):
    albert = []
    for key, group in itertools.groupby(data_sorted, key=lambda x:x[one]):
        a = list(sorted(group, key=lambda item: item[two]))
        suma = sum([f[key] for key in[three] for f in a])
        albert += [sum([f[key] for key in[three] for f in a])]    
    return albert
    pass   


def get_pages(request,paginator):
    page = request.GET.get('page')
    try:
        all_pages = paginator.page(page)
    except PageNotAnInteger:
        all_pages = paginator.page(1)
    except EmptyPage:
        all_pages = paginator.page(paginator.num_pages)
    return all_pages    
    pass


def curent_finace_states(start, end, cursor):
    select_tn_to_pidory = select_docs_to_buyers.format(tn_providers,  "'"+start+"'",  "'"+str(end)+"'")
    select_tn_from_pidory = select_docs_from_providers.format(tn_buyers,  "'"+start+"'",  "'"+str(end)+"'")

    sql_commands_list = (select_tn_to_pidory,select_tn_from_pidory)

    all_docs_tables = [commands.create_list_of_table_values(cursor.execute(f),cursor.description) for f in sql_commands_list]

    summa_poluchenyh_materyalov = [i['summ'] for i in all_docs_tables[1]]
    summa_prodannyh_tovarov = [i['summ'] for i in all_docs_tables[0]]

    usn = str(round(sum(summa_prodannyh_tovarov)*0.05,2))
    nds_polucheny = sum(summa_poluchenyh_materyalov)/6
    nds_otpravleny = sum(summa_prodannyh_tovarov)/6
    full_nds = str (round(nds_otpravleny - nds_polucheny,2))

    return(full_nds, usn)

def get_pays_balance(pp_list, tn_list, element_name):
    pp_suma = sum(float(res[element_name]) for res in pp_list)
    tn_suma = sum(float(res[element_name]) for res in tn_list)

    if pp_suma < tn_suma:
        resultat = 'сумма задолженности контрагента составляет'
        res_sum = str(round(tn_suma-pp_suma,2))
    if pp_suma > tn_suma:
        resultat = 'сумма вашей задолженности составляет'
        res_sum =str(round(pp_suma-tn_suma,2))
    if pp_suma == tn_suma:
        resultat = 'Задолженности нет!'
        res_sum = "Ничего"
    return (resultat,res_sum)
    pass   
