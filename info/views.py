#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from .text_values import *
from django import forms
from django.core.mail import *
import requests

def show_main_page(request):
    about = who
    descript = what_we_did

    contacts = ContList.objects.all()

    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            return render(request, 'landing/thanks.html')
    form = ContactCreateForm()

    return render(request, 'landing/main.html',
    {'form': form,'contacts': contacts, 
    'temp':temp, 'desc':desc, 'icon':icon, 'mainDesc':mainDesc,
    'about':about, 'descript': descript, }) 
