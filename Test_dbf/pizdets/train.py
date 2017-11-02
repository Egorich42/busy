#! /usr/bin/env python
# -*- coding: utf-8 -*
import sqlite3 
base_name = '1.sqlite'
conn = sqlite3.connect(base_name)
cur = conn.cursor()



tn_list = cur.execute("SELECT * FROM docs;").fetchall()

def execution(a,b):
	cur.execute("SELECT summ FROM bank").fetchall()
	pass

a = execution("summ", "bank")
print(a)