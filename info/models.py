#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from .text_values import *
import requests

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(verbose_name='Ваше имя либо название организации', max_length=200)
    address =  models.CharField(verbose_name='Ваша почта', max_length=250)

    def __str__(self):
        return 'Контакты: {}'.format(self.id)


class ContList(models.Model):
    contactDesc = models.CharField(max_length = 100, blank = True, db_index = True, verbose_name = 'Полное имя или номер')
    contactIcon = models.ImageField(upload_to='static/media/', blank=True, verbose_name="Иконка")

    class Meta:
        ordering = ['contactDesc']
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.contactDesc


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


who = texts['who']
why = texts['why']
garanty = texts['garanty']