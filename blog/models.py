#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Post(models.Model):
    post_name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    post_text = models.TextField(blank=True, verbose_name="текст")
    post_image = models.ImageField(upload_to='static/media/', blank=True, verbose_name="Иконка")
    class Meta:
            ordering = ['post_name']
            verbose_name = 'пост'
            verbose_name_plural = 'посты'

    def __str__(self):
        return 'Пост: {}'.format(self.id) +self.post_name