# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-04 11:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client_state', '0006_upload_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
    ]
