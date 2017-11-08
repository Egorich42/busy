#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import *
from .forms import *
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
import sqlite3 
from django.db import migrations
from itertools import groupby
import collections
from collections import defaultdict
from operator import itemgetter
import itertools

#python manage.py version
# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.


class LoginFormView(FormView):
    form_class = AuthenticationForm
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"
    # В случае успеха перенаправим на главную.
    success_url = "/"

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
        return HttpResponseRedirect("/")


def show_user_profile(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        
        base_name = str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()
        
        taxes_system = user.client.nalog_system

        square_fin_states = curent_finace_states(start_square, today, cur, taxes_system)
        month_fin_states = curent_finace_states(start_month, today, cur, taxes_system)

        paginator = Paginator(create_list_of_table_values(cur.execute(select_all_documents),cur.description),15)

        all_documents = get_pages(request,paginator)

        if request.method == 'POST':
            fin_states = FinStatesForm(request.POST)     
            if fin_states.is_valid():
                order = fin_states.save()
                order.save()
          
                start_data = order.start_date
                ending_data = order.end_date

                period_fin_states =curent_finace_states(start_data, ending_data,cur,taxes_system)

            return render(request, 'users/fin_states.html',
                {'start_data':start_data,'ending_data':ending_data,'period_fin_states':str(period_fin_states[0]),'tax_system':period_fin_states[1]})   

        conn.commit()
        conn.close()  

        fin_states = FinStatesForm()
 
        return render(request, 'users/user_profile.html',
        {'all_documents':all_documents, 'month_fin_states':month_fin_states[0],
          'square_fin_states':square_fin_states[0],'fin_states':fin_states,'tax_system':month_fin_states[1]})
    else:
         return HttpResponseRedirect("/")


#!----------https://djbook.ru/ch07s02.html,    
def show_sverka(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        conn = sqlite3.connect(str(user.id)+'.sqlite')
        cur = conn.cursor()

        if request.method == 'POST':
            forma = ContragentIdForm(request.POST)     
            if forma.is_valid():
                order = forma.save()
                order.save()

                start_data = order.start_date
                ending_data = order.end_date

                select_docs_buyers = [select_docs_buyers.format(doc, "'"+str(order.contragent_id)+"'", "'"+start_data+"'", "'"+ending_data+"'") for doc in (pp,tn)]

                all_pp_and_tn = [create_list_of_table_values(cur.execute(doc),cur.description) for doc in (select_docs_buyers)]

                summa_sverki = get_pays_balance(all_pp_and_tn[0], all_pp_and_tn[1], 'summ')

                contr_name = all_tn[0]['name']
                
                return render(request, 'users/sverka_result.html',{'all_pp':all_pp_and_tn[0],
                    'all_tn':all_pp_and_tn[1],'contr_name':contr_name,'start_data':start_data,
                    'ending_data':ending_data,'summa_sverki':summa_sverki})

        forma = ContragentIdForm()
        return render(request, 'users/act_sverki/akt_sverki.html',{'forma': forma})
    else:
         return HttpResponseRedirect("/")   


def show_hvosty(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:

        conn = sqlite3.connect(str(user.id)+'.sqlite')
        cur = conn.cursor()

        if request.method == 'POST':
            hvosty_forma = HvostyForm(request.POST)     
            if hvosty_forma.is_valid():
                order = hvosty_forma.save()
                order.save()
          
                start_data = order.start_date
                ending_data = order.end_date
                
                list_sverok = [get_hvosty_lists(cur,start_data,ending_data)[i] for i in (0,1,2,3)]

                providers_debts = list_sverok[0]
                providers_prepay = list_sverok[1]
                buyers_debts = list_sverok[2]
                buyers_prepay = list_sverok[3]
                
            return render(request, 'users/hvosty/hvosty_result.html',
                {'providers_debts':providers_debts,'providers_prepay':providers_prepay,
                'buyers_debts':buyers_debts, 'buyers_prepay':buyers_prepay, 'start_data':start_data,'ending_data':ending_data })   

        hvosty_forma = HvostyForm()

    return render(request, 'users/hvosty/hvosty.html',{'hvosty_forma':hvosty_forma})
    pass





