#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Contact


class ContactCreateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'address',]

