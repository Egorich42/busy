# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-10 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170306_2053'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([('slug',)]),
        ),
    ]