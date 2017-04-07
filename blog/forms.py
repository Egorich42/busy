#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('post_name','post_text','post_image',)        

