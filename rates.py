import requests
import datetime
from datetime import date
import sqlite3
import os.path

from TESTO import create_list_of_table_values 


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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




def generate_data_list(start_data, end_data):
    start = datetime.datetime.strptime(start_data, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_data, "%Y-%m-%d")

    return [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]


def get_today_course():
    courses_list = []
    for i in [requests.get(nbrb_rates_today.format(x['code_nbrb'])).json() for x in  rates]:
        courses_list += [{"cur_name":i["Cur_Name"],"cur_scale":i["Cur_Scale"],"cur_rate":i["Cur_OfficialRate"] }]
    return courses_list
    pass


class CurrencyUpdater:
    def __init__(self, addres=nbrb_rates_on_date):
       self.addres = addres


    def get_last_update(self):
        conn = sqlite3.connect('courses.sqlite')
        cur = conn.cursor()
        return cur.execute("SELECT data FROM usd").fetchall()[-1][0]
        pass      


    def create_courses_table(self, start_data, money):
       courses_list = []
       for i in [requests.get(self.addres.format(money, data.strftime("%Y-%m-%d"))).json() for data in  generate_data_list(start_data, str(date.today()))]:
           courses_list += [( str(i["Date"][:10]),i["Cur_Name"], i["Cur_Scale"], i["Cur_OfficialRate"] )]
       return courses_list


    def create_courses_lists(self, start_data):
       all_cours_tables = []
       for cours in rates:
           all_cours_tables += [self.create_courses_table(self.get_last_update(), cours['code_nbrb'])]
       return all_cours_tables
       pass


    def updater(self, table, counter):
        conn = sqlite3.connect('courses.sqlite')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table['name'], courses_colls))
        sql_data = cur.execute(select_course_data.format(table['name'])).fetchall()
        if sql_data[-1][0] < str(date.today()):
            cur.executemany(insert_courses.format(table['name']), self.create_courses_lists(sql_data[-1][0])[counter])
            conn.commit()
            conn.close()
            



"""
def full_update():
    for x in range(len(rates)):
        CurrencyUpdater().updater(rates[x], x)


full_update()
"""

#print(get_today_course())

"""
def today_updater():
  all_cours_tables = []
  last_datas = []
  conn = sqlite3.connect('courses.sqlite')
  cur = conn.cursor()
  for i in rates:
      all_cours_tables += [create_list_of_table_values(cur.execute(select_course_data.format(i['name'])),cur.description)]
  conn.commit()
  conn.close()
  for x in range(len(all_cours_tables)):
      if str(date.today()) > all_cours_tables[x][-1]['data']:
          print(str(date.today()))
          cur.executemany(insert_courses.format(table['name']), self.create_courses_lists(sql_data[-1][0])[counter])
print(today_updater())


"""
def today_updater():
    all_cours_tables = []
    last_datas = []
    conn = sqlite3.connect('courses.sqlite')
    cur = conn.cursor()
    datas_table = create_list_of_table_values(cur.execute(select_course_data.format('usd')),cur.description)
    print( str(date.today()), datas_table[-1]['data'])
#    if str(date.today()) > datas_table[-1]['data']:
    
    cur.executemany(insert_courses.format('usd'),  [(str(date.today()), get_today_course()[0]['cur_name'],get_today_course()[0]['cur_scale'],get_today_course()[0]['cur_rate'])])
    conn.commit()
    conn.close()



today_updater()
