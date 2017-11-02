# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-29 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_delete_hvosty_borders'),
    ]

    operations = [
        migrations.AddField(
            model_name='contragent_identy',
            name='title',
            field=models.CharField(blank=True, choices=[('MR', 'Mr.'), ('MRS', 'Mrs.'), ('MS', 'Ms.')], db_index=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='contragent_identy',
            name='contragent_id',
            field=models.CharField(blank=True, db_index=True, max_length=200, verbose_name='Контрагент'),
        ),
        migrations.AlterField(
            model_name='contragent_identy',
            name='end_date',
            field=models.CharField(blank=True, db_index=True, max_length=200, verbose_name='по'),
        ),
        migrations.AlterField(
            model_name='contragent_identy',
            name='start_date',
            field=models.CharField(blank=True, db_index=True, max_length=200, verbose_name='Даты с'),
        ),
    ]