# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 20:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0025_auto_20170203_2314'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='about',
            options={'ordering': ['aboutName'], 'verbose_name': 'О нас', 'verbose_name_plural': 'О нас'},
        ),
    ]
