# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-26 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_state', '0003_auto_20180426_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='file_obj',
        ),
    ]