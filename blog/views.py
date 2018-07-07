#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django import forms

def post_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog/post_list.html', {'posts': posts })


def post_detail(request, slug):
    posts = Post.objects.all().order_by('?')[:4]
    post = get_object_or_404(Post, slug=slug)

    return render(request, 'blog/post.html', {'post':post,'posts': posts })

