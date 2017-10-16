#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Contragent_identy
from .models import *

class ContragentIdForm(forms.ModelForm):
    class Meta:
        model = Contragent_identy
        fields = ['contragent_id','start_date','end_date']

