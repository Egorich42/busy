#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms


class TimePeriodForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))


class ActSverkiForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type':'tel', 'pattern':"[0-9]{4}-[0-9]{2}-[0-9]{2}"}))
    name = forms.CharField(initial='Your name')