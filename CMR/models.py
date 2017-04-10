#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Mails(models.Model):
    mail_head = models.CharField(max_length=200, db_index=True, verbose_name='Тема')
    mail_text = models.TextField(blank=True, verbose_name="текст")

    list_of_clients = ['e.g.hutter@gmail.com','zonaegora@gmail.com']
    from_who = 'e.g.hutter@gmail.com'
    
    class Meta:
            ordering = ['mail_head']
            verbose_name = 'Письма'
            verbose_name_plural = 'Письма'

    def __str__(self):
        return 'Номер: {}'.format(self.id)


class Client(models.Model):
    icon = models.ImageField(upload_to='products/', blank=True, verbose_name="Иконка")
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    description =  models.TextField(blank=True, verbose_name="Описание")
    individual_number = models.PositiveIntegerField(verbose_name='УНН', default=1)
    bank_schet = models.PositiveIntegerField(verbose_name='Банковский счет', default=1)
    spheres= models.CharField(max_length=400, db_index=True, verbose_name='Области деятельности')
    email =  models.EmailField(verbose_name='Е-mail', blank = True) 
    skype= models.CharField(max_length=200, db_index=True, verbose_name='Скайп')
    telegram= models.CharField(max_length=200, db_index=True, verbose_name='Телеграм')
    phone =  models.PositiveIntegerField(verbose_name='Телефон', default=1)

    class Meta:
            ordering = ['name']
            verbose_name = 'Клиенты'
            verbose_name_plural = 'Клиенты'

    def __str__(self):
        return 'Название: {}'.format(self.name)


