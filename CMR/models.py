#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
import requests
# Create your models here.

class Mails(models.Model):
    mail_head = models.CharField(max_length=200, db_index=True, verbose_name='Тема')
    mail_text = models.TextField(blank=True, verbose_name="текст")
    
    class Meta:
            ordering = ['mail_head']
            verbose_name = 'Письма'
            verbose_name_plural = 'Письма'

    def __str__(self):
        return 'Номер: {}'.format(self.id)


class Client(models.Model):
    icon = models.ImageField(upload_to='products/', blank=True, verbose_name="Иконка")
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    organization_type = models.CharField(max_length=50, db_index=True, verbose_name='Вид организации')
    nalog_system = models.CharField(max_length=200, db_index=True, verbose_name='Система налогооблажения')
    unp = models.PositiveIntegerField(verbose_name='УНП', default=1)
    bank_schet = models.CharField(max_length=100, db_index=True,verbose_name='Банковский счет')
    bank_BIK = models.CharField(max_length=100, db_index=True, verbose_name='IBAN')
    email =  models.EmailField(verbose_name='Е-mail', blank = True) 
    skype= models.CharField(max_length=200, db_index=True, blank = True, verbose_name='Скайп')
    phone =  models.PositiveIntegerField(verbose_name='Телефон', blank = True ,default=1)
    

    class Meta:
            ordering = ['name']
            verbose_name = 'Клиенты'
            verbose_name_plural = 'Клиенты'

    def __str__(self):
        return str(self.id) +'. '+self.name 


