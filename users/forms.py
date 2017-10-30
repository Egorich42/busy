#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Contragent_identy

class ContragentIdForm(forms.ModelForm):
    class Meta:
        model = Contragent_identy
        fields = ['contragent_id','start_date','end_date','title']



class HvostyForm(forms.ModelForm):
    class Meta:
        model = Contragent_identy
        fields = ['start_date','end_date']


