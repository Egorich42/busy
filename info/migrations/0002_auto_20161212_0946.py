# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servs',
            name='servDesc',
        ),
        migrations.AddField(
            model_name='servs',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
