#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Contragent_identy

class ContragentIdForm(forms.ModelForm):
    class Meta:
        model = Contragent_identy
        fields = ['contragent_id','start_date','end_date']

class TimePeriodForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))
