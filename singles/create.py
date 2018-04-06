from openpyxl import load_workbook,Workbook
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

filepath = BASE_DIR+'\\'+"test101.xlsx"
wb = openpyxl.Workbook()

wb.save(filepath)