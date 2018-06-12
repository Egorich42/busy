#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
from django.shortcuts import render, get_object_or_404, render_to_response
from users.models import Client
from .models import  return_excel_list, CoursesUpdater, CurrencyStat, CompanyBalance, Hvosty, PortalDifference
from .forms import StateForm, TaxForm, FoundDifferenceForm, CurrStatForm
import sqlite3
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.views.generic.edit import FormView
from django.views.generic.list import ListView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
TO_BASE_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'

from forge import start_month, start_square, today

def get_acess_to_office(request):
	user = request.user.username
	if request.user.username == "busy" or request.user.username =="Egorich42" or request.user.username =="egor":
		clients = []
		for client in Client.objects.all():
			if client.name !='busy' and client.name !='egor' and client.name !='Egorich42':

				clients +=[client]

		return render(request, "singles/clients/clients_list.html", {'clients':clients})
	else:
		return render(request, "singles/clients/office_login_error.html")
	pass


def client_detail(request, name):
	if request.user.username == "busy" or request.user.username =="Egorich42" or request.user.username =="egor":

		client_info = get_object_or_404(Client, name = name)
		tax_system = client_info.nalog_system
		base_name = TO_BASE_PATH+'sqlite_bases'+'\\'+str(client_info.name)+'.sqlite'

		if tax_system == 'nds' or tax_system == 'NDS':

			nds_month_res = CompanyBalance(base_name, "'"+start_month+"'", "'"+ str(today)+"'").count_nds()
			nds_square_res = CompanyBalance(base_name, "'"+start_square+"'", "'"+ str(today)+"'").count_nds()

			nds_month = [{"name": "Входной НДС", "value": str(round(nds_month_res[0],2))},
						{"name": "Исходящий НДС", "value":str(round(nds_month_res[1],2))},
						{"name": "НДС к уплате", "value":str(round(nds_month_res[2],2))}]

			nds_square =  [{"name":"Входной НДС", "value":str(round(nds_square_res[0],2))},
						{"name": "Исходящий НДС", "value":str(round(nds_square_res[1],2))},
						{"name":"НДС к уплате", "value":str(round(nds_square_res[2],2))}]
			usn_month = None
			usn_square = None

		else:
			usn_month = [{"name": "УСН за текущий месяц", "value": str(round(CompanyBalance(base_name, "'"+start_month+"'", "'"+ str(today)+"'").count_usn(),2))}]
			usn_square = [{"name": "УСН за текущий квартал", "value": str(round(CompanyBalance(base_name, "'"+start_square+"'", "'"+ str(today)+"'").count_usn(),2))}]
			nds_month = None
			nds_square = None




		if request.method == 'POST' and 'state_button' in request.POST:
			state_form = StateForm(request.POST, request.FILES)
			if state_form.is_valid():

				data_end = str(state_form.cleaned_data['end_year'])+"-"+str(state_form.cleaned_data["end_month"])+"-"+str(state_form.cleaned_data["end_day"])

				conn = sqlite3.connect(base_name)
				cur = conn.cursor()

				excel_file_name = Hvosty(base_name, "'"+'2016-06-30'+"'",  "'"+ data_end+"'").create_hvosty_excel()

				return return_excel_list(excel_file_name, client_info.name, "hvosty")
				pass




		if request.method == 'POST' and 'tax_button' in request.POST:
			tax_form = TaxForm(request.POST, request.FILES)
	
			if tax_form.is_valid():

				data_start =  str(tax_form.cleaned_data['start_year'])+"-"+str(tax_form.cleaned_data["start_month"])+"-"+str(tax_form.cleaned_data["start_day"])
				data_end = str(tax_form.cleaned_data['end_year'])+"-"+str(tax_form.cleaned_data["end_month"])+"-"+str(tax_form.cleaned_data["end_day"])

				conn = sqlite3.connect(base_name)
				cur = conn.cursor()				

				if tax_system == 'usn' or tax_system == 'USN':
					excel_file_name = CompanyBalance(base_name, "'"+data_start+"'", "'"+data_end+"'").create_tax_excel(CompanyBalance(base_name, "'"+data_start+"'", "'"+data_end+"'").count_usn(),tax_system)
				else:
					excel_file_name = CompanyBalance(base_name, "'"+data_start+"'", "'"+data_end+"'").create_tax_excel(CompanyBalance(base_name, "'"+data_start+"'", "'"+data_end+"'").count_nds(),tax_system)

				return return_excel_list(excel_file_name, client_info.name, "nalog")
				pass




		if request.method == 'POST' and 'found_dif' in request.POST:
			find_difference_form = FoundDifferenceForm(request.POST, request.FILES)

			if 	find_difference_form.is_valid():
				find_difference_form.save()
			
				income_doc_name = find_difference_form.cleaned_data['uploaded_file'].name
				data_start =  str(find_difference_form.cleaned_data['start_year'])+"-"+str(find_difference_form.cleaned_data["start_month"])+"-"+str(find_difference_form.cleaned_data["start_day"])
				data_end = str(find_difference_form.cleaned_data['end_year'])+"-"+str(find_difference_form.cleaned_data["end_month"])+"-"+str(find_difference_form.cleaned_data["end_day"])

				excel_file_name = PortalDifference(base_name =base_name, 
													doc_name = income_doc_name,
													data_start = "'"+ data_start+"'", 
													data_end="'"+data_end+"'",
													request_type = "исходящий").insert_into_excel()

				return return_excel_list(excel_file_name, income_doc_name, "dif")
				pass



		if request.method == 'POST' and 'curr_stat' in request.POST:
			currency_stat_form = CurrStatForm(request.POST, request.FILES)
			if 	currency_stat_form.is_valid():

				data_start =  str(currency_stat_form.cleaned_data['start_year'])+"-"+str(currency_stat_form.cleaned_data["start_month"])+"-"+str(currency_stat_form.cleaned_data["start_day"])
				data_end = str(currency_stat_form.cleaned_data['end_year'])+"-"+str(currency_stat_form.cleaned_data["end_month"])+"-"+str(currency_stat_form.cleaned_data["end_day"])

				excel_file_name = CurrencyStat(base_name = base_name,
											   data_start =data_start,
											   data_end=data_end, 
											   request_type=currency_stat_form.cleaned_data['data_type']).create_statistica_excel()

				if currency_stat_form.cleaned_data['data_type'] == "входящий":
					doc_name = "statistica_vhod"
				if currency_stat_form.cleaned_data['data_type'] == "исходящий":
					doc_name = "statistica_ishod"

				return return_excel_list(excel_file_name, client_info.name, doc_name)

		else:
			tax_form = TaxForm()
			state_form = StateForm()
			find_difference_form = FoundDifferenceForm()
			currency_stat_form = CurrStatForm()

		return render(request, 'singles/clients/client_profile.html', {'client_info':client_info,
																		'state_form': state_form, 
																		'tax_form':tax_form, 
																		"dif_form":find_difference_form,
																		"currency_stat_form":currency_stat_form,
#																		'today_rate': CoursesUpdater().today_updater(),
																		})

	else:
		return render(request, "singles/clients/office_login_error.html")

	pass


