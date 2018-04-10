#! /usr/bin/env python
# -*- coding: utf-8 -*
import mimetypes
import os

from django.shortcuts import render, get_object_or_404, render_to_response
from django.views.generic.edit import View, FormView
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from singles.forms import ArticleForm
from openpyxl import load_workbook,Workbook
from singles import dif 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))+'\\'

def upload_file(request):
	if request.method == 'POST':
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()

			dif.insert_into_excel(request)

			excel_file_name = dif.insert_into_excel(request)
			fp = open(excel_file_name, "rb");
			response = HttpResponse(fp.read());
			fp.close();
			file_type = mimetypes.guess_type(excel_file_name);
			if file_type is None:
				file_type = 'application/octet-stream';
			response['Content-Type'] = file_type
			response['Content-Length'] = str(os.stat(excel_file_name).st_size);
			response['Content-Disposition'] = "attachment; filename = result.xlsx";
#			os.remove(excel_file_name)
			return response;
	else:
		form = ArticleForm()

	return render(request, 'singles/file_upload.html', {'form': form})

