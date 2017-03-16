#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
import urllib.request
import requests

def index(request):
    vid = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet& channelId=UCF0pVplsI8R5kcAqgtoRqoA&key=AIzaSyA0iVygcqhp3YI1pemubZ6y7Jg05UsbIR8')
    vid_js = vid.json()
    items = vid_js['items']
    youtube_addres = "https://www.youtube.com/embed/"
    values = [f['id']['videoId'] for f in items]


    ###################WEATHER###########################
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
    
    ###################WEATHER###########################

    ##########################COURS##########################
    cours = requests.get("http://www.nbrb.by/API/ExRates/Rates?Periodicity=0")
    cours_data = cours.json()

    USD = cours_data[4]
    EUR= cours_data[5]
    RUB=cours_data[16]
    CN='Cur_Name'
    COR='Cur_OfficialRate'
    CS='Cur_Scale'

    cusd = str(USD[CS])+" "+str(USD[CN])+" = "+str(USD[COR])+" руб."
    ceur= str(EUR[CS])+" "+str(EUR[CN])+" = "+str(EUR[COR])+" руб."
    crub= str(RUB[CS])+" "+str(RUB[CN])+" = "+str(RUB[COR])+" руб."
    ##########################COURS##########################
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
    'cusd':cusd, 'crub':crub, 'ceur':ceur,
    'temp':temp, 'desc':desc, 'icon':icon, 'mainDesc':mainDesc, 'values':values,'youtube_addres':youtube_addres}) 
