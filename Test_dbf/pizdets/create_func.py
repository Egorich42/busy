#! /usr/bin/env python
# -*- coding: utf-8 -*

import sqlite3
from dbfread import DBF

def get_data_from_dbf(table_name):
	dataset = list(DBF(table_name, encoding='iso-8859-1'))
	return dataset
	pass


def get_data(table_name, imena_stolbtsov):
	values_list = []
#	vita = [0,1,2,3,4,5]
	via = [t for t in range(len(imena_stolbtsov))]
	for l in table_name:
		values_list+=[[l[imena_stolbtsov[g]] for g in via]]
	return values_list	
	pass


def another_way_to_die(numar, *args):
	urd =[ar for ar in args]
	dot = [0,1,2]
	fiat = []
	for t in dot:
		documents_table = [get_data(numar[t], urd)]
		fiat += [ti for ti in documents_table]
	return fiat	
	pass