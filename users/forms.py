#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Contragent


class ContragentIdForm(forms.ModelForm):
    class Meta:
        model = Contragent
        fields = ['contragent_id']

