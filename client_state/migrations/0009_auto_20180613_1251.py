# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-13 09:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_state', '0008_auto_20180613_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload_file',
            name='end_day',
        ),
        migrations.RemoveField(
            model_name='upload_file',
            name='end_month',
        ),
        migrations.RemoveField(
            model_name='upload_file',
            name='end_year',
        ),
        migrations.RemoveField(
            model_name='upload_file',
            name='start_day',
        ),
        migrations.RemoveField(
            model_name='upload_file',
            name='start_month',
        ),
        migrations.RemoveField(
            model_name='upload_file',
            name='start_year',
        ),
    ]
