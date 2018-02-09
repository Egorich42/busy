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
        return render(request, self.template_name, {'posts': posts,'form': form})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            order = form.save()
            order.save()
            send_mail('Новый клиент', str(order.first_name),  from_who,to_me, fail_silently=False)
            return render(request, 'landing/thanks.html')

            