# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-29 10:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0028_newmail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewMail',
        ),
    ]
