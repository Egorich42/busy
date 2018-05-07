#! /usr/bin/env python
# -*- coding: utf-8 -*
import os
from django.shortcuts import render, get_object_or_404, render_to_response
from users.models import Client
from .models import get_hvosty_lists,create_hvosty_excel, curent_finace_states, create_tax_excel, return_excel_list, insert_into_excel
from .forms import StateForm, TaxForm, FoundDifferenceForm
import sqlite3
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from django.views.generic.edit import FormView
from django.views.generic.list import ListView

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'
TO_BASE_PATH = str('\\'.join(BASE_DIR.split('\\')[:-2]))+'\\'


def get_acess_to_office(request):
	user = request.user.username
	if request.user.username == "busy":
		clients = Client.objects.all()
		return render(request, "singles/clients/clients_list.html", {'clients':clients})
	else:
		return render(request, "singles/clients/office_login_error.html")
	pass


def client_detail(request, name):
	if request.user.username == "busy":

		client_info = get_object_or_404(Client, name = name)

		if request.method == 'POST' and 'state_button' in request.POST:
			state_form = StateForm(request.POST, request.FILES)
			if state_form.is_valid():

				data_start =  "2016-06-30"
				data_end = str(state_form.cleaned_data['end_year'])+"-"+str(state_form.cleaned_data["end_month"])+"-"+str(state_form.cleaned_data["end_day"])

				base_name = TO_BASE_PATH+'sqlite_bases'+'\\'+str(client_info.name)+'.sqlite'
				conn = sqlite3.connect(base_name)
				cur = conn.cursor()

				excel_file_name = create_hvosty_excel(request, get_hvosty_lists(cur,data_start, data_end))
				return return_excel_list(excel_file_name, client_info.name, "hvosty")
				pass


		if request.method == 'POST' and 'tax_button' in request.POST:
			tax_form = TaxForm(request.POST, request.FILES)
	
			if tax_form.is_valid():
				company_name = client_info.id
				tax_system = client_info.nalog_system

				data_start =  str(tax_form.cleaned_data['start_year'])+"-"+str(tax_form.cleaned_data["start_month"])+"-"+str(tax_form.cleaned_data["start_day"])
				data_end = str(tax_form.cleaned_data['end_year'])+"-"+str(tax_form.cleaned_data["end_month"])+"-"+str(tax_form.cleaned_data["end_day"])

				base_name = TO_BASE_PATH+'\\'+'sqlite_bases'+'\\'+str(client_info.name)+'.sqlite'


				conn = sqlite3.connect(base_name)
				cur = conn.cursor()

				excel_file_name = create_tax_excel(request, curent_finace_states(data_start, data_end, cur, tax_system))
				print(tax_system)
				return return_excel_list(excel_file_name, client_info.name, "nalog")
				pass


		if request.method == 'POST' and 'found_dif' in request.POST:
			find_difference_form = FoundDifferenceForm(request.POST, request.FILES)
			if 	find_difference_form.is_valid():
				find_difference_form.save()
			
				income_doc_name = find_difference_form.cleaned_data['uploaded_file'].name
				data_start =  str(find_difference_form.cleaned_data['start_year'])+"-"+str(find_difference_form.cleaned_data["start_month"])+"-"+str(find_difference_form.cleaned_data["start_day"])
				data_end = str(find_difference_form.cleaned_data['end_year'])+"-"+str(find_difference_form.cleaned_data["end_month"])+"-"+str(find_difference_form.cleaned_data["end_day"])

				excel_file_name = insert_into_excel(request, income_doc_name, str(client_info.id),  data_start, data_end, client_info.nalog_system)

				return return_excel_list(excel_file_name, income_doc_name, "div")


		else:
			tax_form = TaxForm()
			state_form = StateForm()
			find_difference_form = FoundDifferenceForm()

		return render(request, 'singles/clients/client_profile.html', {'client_info':client_info,
																		'state_form': state_form, 
																		'tax_form':tax_form, 
																		"dif_form":find_difference_form
																		})

	else:
		return render(request, "singles/clients/office_login_error.html")

	pass

