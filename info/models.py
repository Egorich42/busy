#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Serv(models.Model):
    servName = models.CharField(max_length=200, db_index=True, verbose_name='Название услуги')
    servDescription = models.TextField(blank=True, verbose_name="Описание")
   
    class Meta:
            ordering = ['servName']
            verbose_name = 'Услуги'
            verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.servName

class Price(models.Model):
    priceName = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    priceDescription = models.TextField(blank=True, verbose_name="Описание")
    class Meta:
        ordering = ['priceName']
        verbose_name = 'Цены'
        verbose_name_plural = 'Расценки'

    def __str__(self):
        return self.priceName

class About(models.Model):
    aboutName = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    aboutDescription = models.TextField(blank=True, verbose_name="Описание")
    class Meta:
        ordering = ['aboutName']
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'

    def __str__(self):
        return self.aboutName

class Contact(models.Model):
    first_name = models.CharField(verbose_name='Как к вам обратиться?', max_length=200)
    address =  models.CharField(verbose_name='ваша почта', max_length=250)

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