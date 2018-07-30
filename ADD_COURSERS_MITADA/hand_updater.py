import requests
import datetime
from datetime import date
import sqlite3
import dbf

nbrb_rates_today = "http://www.nbrb.by/API/ExRates/Rates/{}"
nbrb_rates_on_date = "http://www.nbrb.by/API/ExRates/Rates/{}?onDate={}"

rates = [
{'name':'grivna',"code_nbrb": 290}, 
{'name': "usd","code_nbrb": 145}, 
{'name': "eur","code_nbrb": 292},
{'name': "rus","code_nbrb": 298}
]


courses_colls = '(data, name, scale, rate)'
insert_courses = "INSERT INTO {} VALUES (?,?,?,?);"
select_course_period = "SELECT * FROM {} WHERE data >= {} AND  data <= {};"
select_course_data = "SELECT data FROM {} ORDER BY data;"



valute_info = dbf.Table('SC122', codepage='cp1251')

#print(db.field_names)

def get_dbf_valute():
  valute_info.open()
  values_list = {}
  for info in valute_info:
      if info.verstamp != '*':
          values_list[str(info.descr)] = info.id
  valute_info.close()
        
  return values_list   


valute_dbf_vals = get_dbf_valute()

def get_today_course():
    courses_list = []
    courses_list_two = []
    for i in [requests.get(nbrb_rates_today.format(x['code_nbrb'])).json() for x in  rates]:
        cur_id = None
        if i['Cur_ID'] == 298:
            cur_id = valute_dbf_vals['RUB']
        if i['Cur_ID'] == 290:
            cur_id = valute_dbf_vals['UAH']
      
        if i['Cur_ID'] == 145:
            cur_id = valute_dbf_vals['USD']

        if i['Cur_ID'] == 292:
            cur_id = valute_dbf_vals['EUR']

        courses_list += [(cur_id,'U4Y', date.today(),0, str(i["Cur_OfficialRate"]), '0','0','0','0', None )]
        courses_list_two += [(cur_id,'3A', date.today(),0, str(i["Cur_OfficialRate"]/i["Cur_Scale"]), '0','0','0','0', None )]
    return (courses_list, courses_list_two)
    pass




table = dbf.Table('1SCONST', codepage='cp1251')

table.open()


for course in get_today_course()[0]:
    table.append(course)

for course_mult in get_today_course()[1]:
    table.append(course_mult)

