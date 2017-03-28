#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import *
import requests

# Create your views here.
def index(request):
    if request.method == "POST":
        form = MailForm(request.POST)
        clients = Mails.list_of_clients
        from_who = Mails.from_who
        if form.is_valid():

        	
            message_text = "txt"
            subject = 'HI!'
     
            datatuple = (
                 (subject, message_text,  from_who , clients),
             )
            send_mass_mail(datatuple)

    else:
        form = MailForm()

    return render(request, 'mails.html',{'form': form}) 
