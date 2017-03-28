#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import *
import requests

def index(request):
    ##------------------------WEATHER------------------------###
    appid = "55dbe8902d5abb4d0631be757c2a2ba0"
    my_city = 'Minsk, BY'

    res = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Minsk, BY",
                 params={'q': my_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    weathData = {
    'temp': data['main']['temp'],
    'weatherMainDesc': data['weather'][0]['main'],
    'weatherDesc': data['weather'][0]['description'],
    'weatherImg': data['weather'][0]['icon'],
     }

    temp =  str(weathData['temp'])
    desc = str(weathData['weatherDesc'])
    mainDesc = str(weathData['weatherMainDesc'])
    icon = str('http://openweathermap.org/img/w/'+weathData['weatherImg']+'.png')
    
    ##------------------------WEATHER------------------------###
   
    prices = Price.objects.all()
    servs = Serv.objects.all()
    abouts = About.objects.all()
    contacts = ContList.objects.all()
    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            return render(request, 'thanks.html')
    form = ContactCreateForm()

    return render(request, 'main.html',
    {'prices':prices,'servs':servs,'abouts':abouts,'form': form,'contacts': contacts, 
    'temp':temp, 'desc':desc, 'icon':icon, 'mainDesc':mainDesc, }) 
