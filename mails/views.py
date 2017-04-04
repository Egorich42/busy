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

    return render(request, 'mails/mails.html',{'form': form}) 
