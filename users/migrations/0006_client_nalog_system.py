# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-07-04 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180704_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='nalog_system',
            field=models.CharField(blank=True, choices=[('usn', 'usn'), ('nds', 'nds')], db_index=True, max_length=3, verbose_name='Система налогооблажения'),
        ),
    ]