# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-03 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0026_auto_20170203_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contlist',
            options={'ordering': ['contactDesc'], 'verbose_name': 'Контакты', 'verbose_name_plural': 'Контакты'},
        ),
    ]