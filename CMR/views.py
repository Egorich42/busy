#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import *
import requests

def post_email(request):
    if request.method == "POST":
        form = MailForm(request.POST)
        clients = Mails.list_of_clients
        from_who = Mails.from_who
        mail_text = Mails.mail_text
        subject = Mails.mail_head
        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()
     
            datatuple = (
                 (str(post.mail_head), str(post.mail_text),  from_who , clients),
             )
            send_mass_mail(datatuple)
    else:
        form = MailForm()

    return render(request, 'cmr/mails.html',{'form': form}) 


#python manage.py migrate --run-syncdb

def create_client(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        if form.is_valid():
            client = client_form.save(commit=False)
            client.author = request.user
            client.save()
    else:
        client_form = ClientForm()
        

    return render(request, 'cmr/create_client.html', {'client_form': client_form}) 


def client_list(request):
    clients = Client.objects.all().order_by('id')

    return render(request, 'cmr/clients_list.html', {'clients': clients })



def client_profile(request, id):
    client = get_object_or_404(Client, id=id)

    return render(request, 'cmr/client.html', {'client':client})
