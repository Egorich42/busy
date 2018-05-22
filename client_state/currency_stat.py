nbrb_rates_today = "http://www.nbrb.by/API/ExRates/Rates/{}"
nbrb_rates_on_date = "http://www.nbrb.by/API/ExRates/Rates/{}?onDate={}"


rates = [
{'name':'grivna',"code_nbrb": 290, 'request':sq_c.select_grivn_course, 'base_id': '4'}, 
{'name': "usd","code_nbrb": 145, 'request':sq_c.select_usd_course, 'base_id': '7'}, 
{'name': "eur","code_nbrb": 292, 'request':sq_c.select_eur_course, 'base_id': '3'},
{'name': "rus","code_nbrb": 298, 'request':sq_c.select_rus_course, 'base_id': '6'}
]




def generate_data_list(start_data, end_data):
    start = datetime.datetime.strptime(start_data, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_data, "%Y-%m-%d")
    return [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    pass


def get_today_course(addres):
    courses_list = []
    for i in [requests.get(addres.format(x['code_nbrb'])).json() for x in  rates]:
        courses_list += [{"cur_name":i["Cur_Name"],"cur_scale":i["Cur_Scale"],"cur_rate":i["Cur_OfficialRate"] }]
    return courses_list
    pass


def create_courses_table(addres, money):
    courses_list = []

    for i in [requests.get(addres.format(money, data.strftime("%Y-%m-%d"))).json() for data in  generate_data_list("2018-01-01", str(date.today()))]:
        courses_list += [( str(i["Date"][:10]),i["Cur_Name"], i["Cur_Scale"], i["Cur_OfficialRate"] )]
    return courses_list
    pass


def update_courses_base(table, income_list):
    conn = sqlite3.connect('courses.sqlite')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table['name'], courses_colls))
    cur.executemany(insert_courses.format(table['name']), income_list)
    conn.commit()
    conn.close()
    pass



def valuty_sql_to_list(base_name, select_comand, data_start, data_end):
    conn = sqlite3.connect(base_name)
    cur = conn.cursor()
    sql_request = select_comand.format(data_start, data_end)

    return create_list_of_table_values(cur.execute(sql_request),cur.description)
    pass



def currency_docs_counter(data_start, data_end, base_name):
    count =[]
    for i in valuty_sql_to_list(base_name, sq_c.select_valuty_income, data_start, "'"+data_end+"'"):
        if i['doc_date'] >= data_start and i['doc_date'] <= data_end:
            count+=[{'date':i['doc_date'], 'document': i['document_name'], 'summ': i['summ'],'contragent':i['contragent_name'], 'currency_type':i['currency_type'], }]
    return count
    pass



def statistika(currency, data_start, data_end, base_name):
    result = []
    for x in currency_docs_counter(data_start, data_end, base_name):
        for y in valuty_sql_to_list('courses.sqlite', currency['request'], "'"+data_start+"'", "'"+data_end+"'" ):
            if y['data'] == x['date']:
                if x['currency_type'] == currency['base_id']:
                    result +=  [{
                                'контрагент':x['contragent'],
                                'дата': y['data'],
                                'курс на дату документа':y['rate'], 
                                'сумма в рублях':x['summ']*y['rate'],
                                'дата': y['data']
                                }]
    return result

    pass          




def return_final_statistica(data_start, data_end, base_name):
    final_list = []
    for x in range(len(rates)):
        final_list += [statistika(rates[x],data_start, data_end, base_name)]
    return final_list    







def create_statistica_excel(request, base_name, data_start, data_end):
    output_doc = BASE_DIR+"tax_result.xlsx"
    openpyxl.Workbook().save(output_doc)
    output_list = load_workbook(output_doc,data_only = True)
    main_out_sheet = output_list.active  


    income_list = return_final_statistica(data_start, data_end, base_name)


    def insert_cell(row_val, col_val, cell_value):
        main_out_sheet.cell(row = row_val, column = col_val).value = cell_value
        pass  

    insert_cell(1, 1, "Дата")
    insert_cell(1, 2, "Контрагент")
    insert_cell(1, 3, "Валюта")
    insert_cell(1, 3, "Страна")
    insert_cell(1, 4, "Сумма в валюте")
    insert_cell(1, 5, "Сумма в бел. рублях")


    
    for i in range(len(income_list[2])):
        insert_cell(i+1, 1, income_list[2][i]['дата'])
        insert_cell(i+1, 2, income_list[2][i]['контрагент'])
        insert_cell(i+1, 3, income_list[2][i]['курс на дату документа'])
        insert_cell(i+1, 4, income_list[2][i]['сумма в рублях'])

        output_list.save(filename = output_doc)
    return(str(output_doc))
    pass









#---------------------------------STATISTIKA End----------------


