#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import send_mass_mail,send_mail
import requests


from django.views.generic.edit import FormView
from django.views.generic.base import View

class MainPageView(View):
    form_class = ContactCreateForm
    template_name = 'landing/main.html'
    initial = {'key': 'value'}
    

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

            
def show_demo(request):
    return render(request, 'landing/demo.html')          