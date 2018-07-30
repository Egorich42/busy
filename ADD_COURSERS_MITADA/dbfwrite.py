import dbf
from openpyxl import load_workbook,Workbook
from hand_updater import get_today_course


table = dbf.Table('1SCONST', codepage='cp1251')

table.open()


from datetime import date
print(date.today())
#print(get_today_course())

#print(get_today_course()[0].values())
for datum in ( ('  3','U4Y', date.today(), 0, '3.2508'),  ):
    table.append(datum)





#		0,0,0,0, None