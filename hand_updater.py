import requests
import datetime
from datetime import date
import sqlite3
import os.path

from forge import create_list_of_table_values 


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


    def create_courses_table(self, money):
       courses_list = []
       for i in [requests.get(self.addres.format(money, data.strftime("%Y-%m-%d"))).json() for data in  generate_data_list( '2018-06-11', '2018-07-17')]:
           courses_list += [( str(i["Date"][:10]),i["Cur_Name"], i["Cur_Scale"], i["Cur_OfficialRate"] )]
       return courses_list


    def create_courses_lists(self):
       all_cours_tables = []
       for cours in rates:
           all_cours_tables += [self.create_courses_table(cours['code_nbrb'])]
       return all_cours_tables
       pass


    def courses_updater(self, table, counter):
        conn = sqlite3.connect('courses.sqlite')
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format(table['name'], courses_colls))
        sql_data = cur.execute(select_course_data.format(table['name'])).fetchall()
        cur.executemany(insert_courses.format(table['name']), self.create_courses_lists()[counter])
        conn.commit()
        conn.close()
        pass
            


def full_update():
    for x in range(len(rates)):
        CurrencyUpdater().courses_updater(rates[x], x)


full_update()



#print(CurrencyUpdater().create_courses_lists())

#CurrencyUpdater().today_updater()
