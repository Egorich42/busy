import win32com.client

Excel = win32com.client.Dispatch("Excel.Application")
#wb = Excel.Workbooks.Open(u'D:\\BUS\\busy\\Test_dbf\\dipart.xls')
#first_list = Excel.Workbooks.Open(u'D:\\Bysy\\Busy\\singles\\transkom_in.xls')
first_list = Excel.Workbooks.Open(u'D:\BUS\Busy\singles\\transkom_in.xls')

united= Excel.Workbooks.Open(u'D:\BUS\Busy\singles\\united.xls')
mitada= Excel.Workbooks.Open(u'D:\BUS\Busy\singles\\mitada.xls')
bona= Excel.Workbooks.Open(u'D:\BUS\Busy\singles\\bona.xls')


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


mitada_dataset = mitada.ActiveSheet
united_dataset = united.ActiveSheet
bona_dataset = bona.ActiveSheet

names_list = [i['name'] for i in create_first_arenda_list()]
have_nds_list = [i[have_nds] for i in create_first_arenda_list()]

#записываем последовательность
i = 5
for rec in names_list:
    mitada_dataset.Cells(i,1).value = rec
    i = i + 1

m = 5
for rec in have_nds_list:
    mitada_dataset.Cells(m,2).value = rec
    m = m + 1

#сохраняем рабочую книгу
mitada.Save()

#закрываем ее
mitada.Close()

#закрываем COM объект
Excel.Quit()
#сохраняем рабочую книгу
#wb.Save()

#закрываем ее
#wb.Close()

#закрываем COM объект
Excel.Quit()
