#! /usr/bin/env python
# -*- coding: utf-8 -*

from datetime import *
import itertools
from itertools import groupby
from operator import itemgetter
import sqlite3
import os



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

taxes = (('УСН', 'усн.'),('НДС', 'ндс.'),)

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


def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 

