#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import *
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
import sqlite3 

#https://djbook.ru/examples/39/
#https://ustimov.org/posts/17/
#http://acman.ru/django/publichnyi-profil-i-lichnyi-kabinet-po-odnoi-ssylk/

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login

class LoginFormView(FormView):
    form_class = AuthenticationForm
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/users/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)



class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)
        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")



def show_user_profile(request,id, **kwargs):
    user = get_object_or_404(User, id=id)

    if user == request.user:
    
        base_name = str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()


        bank1 = cur.execute("""
        SELECT summ
        FROM bank;
        """).fetchall()

        bank2 = list(bank1[0])
        bank = str(bank2[0])

        tn_list= cur.execute("""
        SELECT *
        FROM docs;
        """).fetchall()

        conn.close()

        nakladnye = [list(elem) for elem in tn_list]
        cols = [column[0] for column in cur.description]
        res = []
        for row in nakladnye:
            res += [{col.lower():value for col,value in zip(cols,row)}] 

   
        return render(request, 'users/user_profile.html',
        { 'bank':bank,'res':res,})
    else:
         return HttpResponseRedirect("/")   


def UsersList(request):
	users = User.objects.all()
	return render(request, 'users/users_list.html', {'users':users})
	pass




