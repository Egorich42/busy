#! /usr/bin/env python
# -*- coding: utf-8 -*
import win32com.client
import os
import xlwt
import numpy as np


Excel = win32com.client.Dispatch("Excel.Application")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'


def find_first_point(dataset):
	for i in range(1,10):
		if dataset.Cells(i,3).value != None and dataset.Cells(i,2).value == 1.0:
			dataset.Cells(i,2).value
			return i
			pass


def find_endpoint(dataset,start,cell_text):
	for i in range(start,510):
		if dataset.Cells(i,5).value ==str(cell_text):
			return i-1
			pass


def get_input_data(doc_name):
	Excel = win32com.client.Dispatch("Excel.Application")
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
	document = Excel.Workbooks.Open(BASE_DIR+doc_name)
	active_list_on_documnent = Excel.Workbooks.Open(BASE_DIR+doc_name).ActiveSheet
	return (document, active_list_on_documnent)
	pass




def excol_to_list(dataset_name, col_name, interval):
	list_name = [r[0].value for r in dataset_name.Range(interval.format(col_name,col_name))]
	return list_name
	pass


