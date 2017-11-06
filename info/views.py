#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import send_mass_mail,send_mail
import requests

def show_main_page(request):
    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
        new_name = Contact.first_name

        if form.is_valid():
            order = form.save()
            order.save()
 
            send_mail('Новый клиент', str(order.first_name),  from_who,
                to_me, fail_silently=False)

            return render(request, 'landing/thanks.html')
    form = ContactCreateForm()

    return render(request, 'landing/main.html',
    {'form': form}) 
    
def show_contacts_page(request):
    return render(request, 'landing/contacts.html') 