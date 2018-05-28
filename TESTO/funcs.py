from operator import itemgetter

import datetime
from datetime import date
import os
import sqlite3
import itertools
from django.http import HttpResponse, HttpResponseRedirect
import mimetypes



BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'


def sum_of_list(sum_name,income_list):
    return sum([x[sum_name] for x in income_list])
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



def return_excel_list(income_file, client_name, doc_type):
    fp = open(income_file, "rb")
    response = HttpResponse(fp.read())
    fp.close()
    file_type = mimetypes.guess_type(income_file)
    if file_type is None:
        file_type = 'application/octet-stream'
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(income_file).st_size)
    response['Content-Disposition'] = "attachment; filename = {}-{}.xlsx".format(client_name,doc_type)
    os.remove(income_file)
    return response


def generate_data_list(start_data, end_data):
    start = datetime.datetime.strptime(start_data, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_data, "%Y-%m-%d")
    return [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    pass
