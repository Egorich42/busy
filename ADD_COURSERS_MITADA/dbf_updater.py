import requests
import datetime
from datetime import date
import sqlite3
import dbf



valute_info = dbf.Table('SC122', codepage='cp1251')

#print(db.field_names)

def get_dbf_valute():
  valute_info.open()
  values_list = []
  for info in valute_info:
      if info.ismark != '*' and info.descr != 'BYN'and info.descr != 'LTL':
          values_list += [info.descr]
  valute_info.close()
        
  return values_list

print(get_dbf_valute())


'''
table = dbf.Table('1SCONST', codepage='cp1251')

table.open()


for course in get_today_course()[0]:
    table.append(course)

for course_mult in get_today_course()[1]:
    table.append(course_mult)
'''