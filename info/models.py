#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import requests

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(verbose_name='Ваша почта или телефон', max_length=200)

    def __str__(self):
        return 'Контакты: {}'.format(self.id)


"""
appid = "55dbe8902d5abb4d0631be757c2a2ba0"
my_city = 'Minsk, BY'
weather_request =  "http://api.openweathermap.org/data/2.5/weather?q="
weathe_icons = 'http://openweathermap.org/img/w/'

to_me = ['e.g.hutter@gmail.com']
from_who = 'e.g.hutter@gmail.com'

res = requests.get(weather_request+my_city,
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
icon = str(weathe_icons+weathData['weatherImg']+'.png')
"""


