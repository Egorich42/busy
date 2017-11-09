#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
import selector
from selector import *


wb = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\dipart.xls')
sheet = wb.ActiveSheet



#получаем значение первой ячейки

#val = sheet.Cells(1,1).value

#sheet.Cells(1,2).value = val

#записываем последовательность
def nuts(some_list,some_list1,some_list2,some_list3, col_name):
    cell_number = 1
    for rec in some_list:
        sheet.Cells(1,col_name).value = "Задолженность поставщиков"
        sheet.Cells(cell_number,col_name).value = rec
        cell_number = cell_number + 1    
        pass
        

    cell_number1 = len(some_list)+5
    sheet.Cells(cell_number1-2,col_name).value = "Предоплата поставщикам"
    for rec1 in some_list1:
        sheet.Cells(cell_number1,col_name).value = rec1
        cell_number1 = cell_number1 + 1    
        pass


    cell_number2 = (len(some_list1)+5+len(some_list)+5)
    sheet.Cells(cell_number2-2,col_name).value = "Задолженность покупателей"
    for rec2 in some_list2:
        sheet.Cells(cell_number2,col_name).value = rec2
        cell_number2 = cell_number2 + 1    
        pass


    cell_number3 = (len(some_list)+5+len(some_list1)+5+len(some_list2)+5)
    sheet.Cells(cell_number3-2,col_name).value = "Предоплата от покупателей"

    for rec3 in some_list3:
        sheet.Cells(cell_number3,col_name).value = rec3
        cell_number3 = cell_number3 + 1    
        pass                


nuts(debts_providers_sums,prepayment_providers_sums,debts_buyers_sums,prepayment_buyers_sums,2)
nuts(debts_providers_names,prepayment_providers_names,debts_buyers_names,prepayment_buyers_names,1)


#сохраняем рабочую книгу
wb.Save()

#закрываем ее
wb.Close()

#закрываем COM объект
Excel.Quit()