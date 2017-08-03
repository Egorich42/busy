#! /usr/bin/env python
# -*- coding: utf-8 -*

#https://djbook.ru/examples/39/

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



def show_user_profile(request,id):
    user = get_object_or_404(User, id=id)

    base_name = str(user.id)+'.sqlite'

    conn = sqlite3.connect(base_name)
    cur = conn.cursor()

    bank = cur.execute("""
    SELECT summ
    FROM bank;
    """).fetchall()

    tn_sum = cur.execute("""
    SELECT sum
    FROM tn;
    """).fetchall()


    tn_contr= cur.execute("""
    SELECT *
    FROM tn;
    """).fetchall()

    conn.close()
    beta = str(bank)
    
    t_sum = str(tn_sum)

    t_kontr = str(tn_contr)


    return render(request, 'users/user_profile.html',
        {'t_sum':t_sum, 't_kontr':t_kontr})




def UsersList(request):
	users = User.objects.all()
	return render(request, 'users/users_list.html', {'users':users})
	pass




