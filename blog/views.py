#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.shortcuts import redirect

from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms
from django.core.mail import *
import requests

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts })




def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'post.html',
                             {'post': post})


def PostDetail(request, id, slug):
    post = get_object_or_404(Post, id=id)


def create_post(request):
    if request.method == "POST":
        form = Post_Form(request.POST)
        if form.is_valid():
           post = form.save(commit=False)
           post.author = request.user
           post.save()

           return redirect('post_detail',id=id)
    else:
    	form = Post_Form()	

    return render(request, 'create_post.html',{'form': form}) 
