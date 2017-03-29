#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import *

class Post_Form(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('post_name', 'post_text',)