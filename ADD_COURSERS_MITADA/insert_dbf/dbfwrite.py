import dbf
from openpyxl import load_workbook,Workbook



table = dbf.Table('SC245', codepage='cp1251')

table.open()


for datum in( ('1VCIB','0','1532','педро Polishing Kit'),  ):
    table.append(datum)
