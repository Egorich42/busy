# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-29 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_name', models.CharField(db_index=True, max_length=200, verbose_name='Название')),
                ('post_text', models.TextField(blank=True, verbose_name='текст')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
                'ordering': ['post_name'],
            },
        ),
    ]
