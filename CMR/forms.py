#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import *

class MailForm(forms.ModelForm):

    class Meta:
        model = Mails
        fields = ('mail_head', 'mail_text',)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('icon','name', 'description','individual_number','bank_schet', 'spheres','email', 'skype', 'telegram','phone',)        

