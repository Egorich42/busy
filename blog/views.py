#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
import requests
 
#python manage.py migrate --run-syncdb
def create_post(request):
    if request.method == "POST":
        client_form = PostForm(request.POST)
        if form.is_valid():
            client = client_form.save(commit=False)
            client.author = request.user
            client.save()
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'client_form': client_form}) 


def post_list(request):
    posts = Post.objects.all().order_by('name')

    return render(request, 'blog/post_list.html', {'posts': posts })

def client_profile(request):
    return render(request, 'blog/post.html')