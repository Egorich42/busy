# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-16 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171016_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hvosty_borders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docunent_start_data', models.CharField(blank=True, db_index=True, max_length=200, verbose_name='start_date')),
                ('docunent_end_data', models.CharField(blank=True, db_index=True, max_length=200, verbose_name='end_date')),
            ],
        ),
    ]