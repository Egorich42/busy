#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import requests

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(verbose_name='Ваша почта или телефон', max_length=200)
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



texts = {
"who": '"Бухгалтерские советы" - компания, на удаленной основе оказывающая услуги в области ведения кадровой, налоговой и бухгалтерской документации, а так же консультирующая по вопросам ведения и открытия бизнеса.',
"what_we_did":"Мы берем на себя довольно затратную и объемную часть бизнеса - ведение финансовой и кадровой документации, подготовку различной финансовой отчетности, прохождение и представление ваших интересов во время финансовых проверок. \n Оказываем свои услуги на удаленной основе, что означает для вас целый ряд преимуществ перед наймом штатных специалистов - нет нужды оборудовать рабочие места, выплачивать страховые и социальные взносы, а так же задумываться об отпуске и больничном. Вместо этого штат опытных бухгалтеров, занимающихся вашими делами, что кушать не просят и места не занимают.",
}

who = texts['who']
what_we_did = texts['what_we_did']


def list_of_table_values(request_name):
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in cur.description]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 

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


