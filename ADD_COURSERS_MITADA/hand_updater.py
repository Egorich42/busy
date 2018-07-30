import requests
import datetime
from datetime import date
from datetime import datetime

import sqlite3
import dbf

nbrb_rates_today = "http://www.nbrb.by/API/ExRates/Rates/{}?ParamMode=1"


rates = [
{'name':'grivna',"code_nbrb": 290,'cur_code':980, 'cur_abbrev': 'UAH'}, 
{'name': "usd","code_nbrb": 145,'cur_code':840, 'cur_abbrev': 'USD'}, 
{'name': "eur","code_nbrb": 292,'cur_code':978, 'cur_abbrev': 'EUR'}, 
{'name': "rus","code_nbrb": 298,'cur_code':643, 'cur_abbrev': 'RUB'},
{'name': "ch_cron","code_nbrb": 171,'cur_code':203, 'cur_abbrev': 'CZK'}, 
{'name': "sw_frn","code_nbrb": 130,'cur_code':756, 'cur_abbrev': 'CHF'}, 
{'name': "pol_zlt","code_nbrb": 188,'cur_code':985, 'cur_abbrev': 'PLN'}, 
]



courses_colls = '(data, name, real_rate, rate, scale)'
insert_courses = "INSERT INTO rates VALUES (?,?,?,?,?);"
select_course_data = "SELECT data FROM rates ORDER BY data;"



def get_today_courses():
    courses_list = []
    for i in [requests.get(nbrb_rates_today.format(x['cur_code'])).json() for x in  rates]:
        courses_list += [(i["Date"][:10], str( i['Cur_Abbreviation']), float(i["Cur_OfficialRate"])/ int(i["Cur_Scale"]), float(i["Cur_OfficialRate"]), int(i["Cur_Scale"]), )]
    return courses_list
    pass


def courses_updater():
    conn = sqlite3.connect('courses.sqlite')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS {} {}".format("rates", courses_colls))
    last_base_date = datetime.strptime(cur.execute(select_course_data).fetchone()[0], "%Y-%m-%d").date()
    if type(last_base_date) == None or last_base_date < date.today():
        for x in get_today_courses():
            cur.execute(insert_courses, x)
    if last_base_date == date.today():
        return True
    conn.commit()
    conn.close()
    pass


courses_updater()