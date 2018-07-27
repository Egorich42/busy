import dbf
from openpyxl import load_workbook,Workbook
from hand_updater import get_today_course


table = dbf.Table('1SCONST', codepage='cp1251')

table.open()

#print(get_today_course()[0].values())
for datum in( {'  3','U4Y', None, 0, '3.2508'},  ):
    table.append(datum)





