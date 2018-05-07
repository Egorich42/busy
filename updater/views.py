from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from .models import bazi, full_update

def update_bases(request):
    for i in range(len(bazi)):
        full_update(i,bazi[i])
        
    return HttpResponseRedirect("/")
