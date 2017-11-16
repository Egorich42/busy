import win32com.client

Excel = win32com.client.Dispatch("Excel.Application")
#wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart.xls')
first_list = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\singles\\transkom_in.xls')
#united_list = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\test_dbf\\united.xls')
#mitada_list = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\test_dbf\\mitada.xls')
#bona_list = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\test_dbf\\bona.xls')


first_dataset = first_list.ActiveSheet

company_list = ('united', 'mitada','bona_kauza')
names_cells = [r[0].value for r in first_dataset.Range("B2:B14")]
price_cells = [r[0].value for r in first_dataset.Range("C2:C14")]
nds_cells = [r[0].value for r in first_dataset.Range("D2:D14")]

def create_first_arenda_list():
	list_length = list(range(len(names_cells))) 
	arenda_list=[]
	list_of_lists = (names_cells, price_cells,nds_cells)
	for i in list_length:
		arenda_dict = {'name':list_of_lists[0][i], 'price':list_of_lists[1][i], 'have_nds':list_of_lists[2][i]}
		arenda_list += [arenda_dict]
		pass
	return arenda_list
	pass


def create_all_lists():
	rent_parameters = create_first_arenda_list()
	rent_list=[]
	mnojitel = [0.1984, 0.1522, 0.1111]

	for m in mnojitel:

		arendator_price = [round(i['price']*m, 2) for i in rent_parameters if type(i['price'])==float]
		final_count_nds = [round(i['price']*m*0.2,2) for i in rent_parameters if type(i['price'])==float]
		final_count = [round(i['price']*m*1.2,2) for i in rent_parameters if type(i['price'])==float]

		sum_price = round(sum(arendator_price),2)
		sum_nds =  round(sum(final_count_nds),2)
		sum_funal_count =  round(sum(final_count),2)

		rent_list +=[([i for i in arendator_price],[i for i in final_count_nds],[i for i in final_count],(sum_price,sum_nds,sum_funal_count))]

	return rent_list
	pass





create_all_lists()[i][]

[
(
[29.95, 9.43, 2.03, 0.35, 0.83, 5.36, 0.16, 0.05, 10.75, 2.31, 0.88, 0.65], 
[5.99, 1.89, 0.41, 0.07, 0.17, 1.07, 0.03, 0.01, 2.15, 0.46, 0.18, 0.13], 
[35.95, 11.32, 2.44, 0.42, 1.0, 6.44, 0.19, 0.06, 12.9, 2.77, 1.06, 0.78], 
(62.75, 12.56, 75.33)
), 

(
[22.98, 7.24, 1.56, 0.27, 0.64, 4.11, 0.12, 0.04, 8.25, 1.77, 0.68, 0.5], 
[4.6, 1.45, 0.31, 0.05, 0.13, 0.82, 0.02, 0.01, 1.65, 0.35, 0.14, 0.1], 
[27.57, 8.68, 1.87, 0.33, 0.77, 4.94, 0.14, 0.04, 9.9, 2.12, 0.81, 0.6], 
(48.16, 9.63, 57.77)
), 

(
[16.77, 5.28, 1.14, 0.2, 0.47, 3.0, 0.09, 0.03, 6.02, 1.29, 0.5, 0.37], 
[3.35, 1.06, 0.23, 0.04, 0.09, 0.6, 0.02, 0.01, 1.2, 0.26, 0.1, 0.07], 
[20.13, 6.34, 1.36, 0.24, 0.56, 3.6, 0.11, 0.03, 7.23, 1.55, 0.59, 0.44], 
(35.16, 7.03, 42.18)
)

]

#записываем значение в определенную ячейку
sheet.Cells(1,2).value = val

#записываем последовательность
i = 1
for rec in vals:
    sheet.Cells(i,3).value = rec
    i = i + 1

#сохраняем рабочую книгу
wb.Save()

#закрываем ее
wb.Close()

#закрываем COM объект
Excel.Quit()
#сохраняем рабочую книгу
#wb.Save()

#закрываем ее
#wb.Close()

#закрываем COM объект
Excel.Quit()