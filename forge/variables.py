#! /usr/bin/env python
# -*- coding: utf-8 -*

from datetime import *
import itertools
from itertools import groupby
from operator import itemgetter
import sqlite3
import os

from .requests import select_grivn_course, select_usd_course, select_eur_course, select_rus_course

today = date.today()
this_year = date.today().year
this_month = date.today().month

first_kvartal_end = date(this_year, 3,31)
second_kvartal_end= date(this_year,6,30)
third_kvartal_end= date(this_year,9,30)
four_kvartal_end = date(this_year,12,31)


first_kvartal_start = date(this_year, 1,1)
second_kvartal_start= date(this_year,4,1)
third_kvartal_start= date(this_year,7,1)
four_kvartal_start = date(this_year,10,1)

taxes = (('usn', 'usn'),('nds', 'nds'),)

def current_kvartal():
    if today<first_kvartal_end:
        cur_kvart = first_kvartal_start
    if today > first_kvartal_end and today < second_kvartal_end:
        cur_kvart = second_kvartal_start
    if today >third_kvartal_start and today <third_kvartal_end:
        cur_kvart = third_kvartal_start
    if today > four_kvartal_start and today < four_kvartal_end:
        cur_kvart = four_kvartal_start    
        pass
    return cur_kvart
    pass 


start_square = str(current_kvartal())
start_month = str(date(this_year, this_month, 1))

nbrb_rates_today = "http://www.nbrb.by/API/ExRates/Rates/{}"
nbrb_rates_on_date = "http://www.nbrb.by/API/ExRates/Rates/{}?onDate={}"


rates = [
{'name':'grivna',"code_nbrb": 290, 'request':select_grivn_course, 'base_id': '4'}, 
{'name': "usd","code_nbrb": 145, 'request':select_usd_course, 'base_id': '7'}, 
{'name': "eur","code_nbrb": 292, 'request':select_eur_course, 'base_id': '3'},
{'name': "rus","code_nbrb": 298, 'request':select_rus_course, 'base_id': '6'}
]



years = [("2018", "2018"),("2017", "2017"),("2016", "2016"), ("2015", "2015"),]


months = [ ("01", "январь", ),("02", "февраль", ),("03",  "март"),( "04","апрель"),("05", "май" ), ("06","июнь"),
            ("07", "июль"),("08", "август"),("09", "сентябрь"), ("10", "октябрь"),("11", "ноябрь"),
            ("12", "декабрь")]



days = [("01","01"), ("02","02"), ("03","03"), ("04","04"), ("05","05"), ("06","06"), ("07","07"), 
        ("08","08"), ("09","09"), ("10","10"), ("11","11"), ("12","12"), ("13","13"),  
        ("14","14"), ("15","15"), ("16","16"), ("17","17"), ("18","18"), ("19","19"),
        ("20","20"), ("21","21"), ("22","22"), ("23","23"), ("24","24"), ("25","25"), 
        ("26","26"),  ("27","27"),("28","28"), ("29","29"),  ("30","30"),  ("31", "31"), ]