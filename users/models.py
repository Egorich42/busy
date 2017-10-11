#! /usr/bin/env python
# -*- coding: utf-8 -*

#https://habrahabr.ru/post/313764/

from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    organization_type = models.CharField(max_length=50, db_index=True, verbose_name='Вид организации')
    nalog_system = models.CharField(max_length=200, db_index=True, verbose_name='Система налогооблажения')
    unp = models.PositiveIntegerField(verbose_name='УНП', default=1)
    bank_schet = models.CharField(max_length=100, db_index=True,verbose_name='Банковский счет')
    bank_BIK = models.CharField(max_length=100, db_index=True, verbose_name='IBAN')
    email =  models.EmailField(verbose_name='Е-mail', blank = True) 
    skype= models.CharField(max_length=200, db_index=True, blank = True, verbose_name='Скайп')
    phone =  models.PositiveIntegerField(verbose_name='Телефон', blank = True ,default=1)



    