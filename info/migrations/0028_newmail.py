# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-27 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0027_auto_20170203_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='Имя')),
                ('address', models.CharField(max_length=250, verbose_name='Текст письма')),
            ],
        ),
    ]
