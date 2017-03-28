# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-27 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_head', models.CharField(db_index=True, max_length=200, verbose_name='Тема')),
                ('mail_text', models.CharField(db_index=True, max_length=200, verbose_name='Текст')),
            ],
            options={
                'ordering': ['mail_head'],
                'verbose_name_plural': 'Письма',
                'verbose_name': 'Письма',
            },
        ),
    ]
