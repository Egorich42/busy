# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-07 11:17
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20170410_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='story',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Текст'),
        ),
    ]