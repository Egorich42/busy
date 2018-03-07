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

from django.contrib.auth import authenticate, login
import os


import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
        
        base_name = BASE_DIR+'\\'+str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()
        taxes_system = user.client.nalog_system

        square_fin_states = curent_finace_states(start_square, var.today, cur, taxes_system)
        month_fin_states = curent_finace_states('2017-12-01', '2017-12-31', cur, taxes_system)

        all_pp_buyers = np.array(get_paginator(cur, 'contragents_documents_two',sq_c.pp_buyers,15,request))
        all_buyers_docs = np.array(get_paginator(cur, 'contragents_documents_two',sq_c.tn_buyers,15,request))
        all_pp_providers = np.array(get_paginator(cur, 'contragents_documents',sq_c.pp_providers,15,request))
        all_providers_docs = np.array(get_paginator(cur, 'contragents_documents',sq_c.tn_providers,15,request))

        
#        hvosty_list = get_hvosty_lists(cur,'2016-06-30',str(var.today))
        hvosty_list = get_hvosty_lists(cur,'2016-06-30','2017-12-31')

        providers_debts = hvosty_list[0]
        providers_prepay = hvosty_list[1]
        buyers_debts = hvosty_list[2]
        buyers_prepay = hvosty_list[3]
    
        providers_debts_result = hvosty_list[4]
        providers_prepay_result = hvosty_list[5]
        buyers_debts_result = hvosty_list[6]
        buyers_prepay_result = hvosty_list[7]


        if request.method == 'POST':
            fin_states = TimePeriodForm(request.POST)     
            if fin_states.is_valid():
                start_data = str(fin_states.cleaned_data['start_date'])
                ending_data = str(fin_states.cleaned_data['end_date'])

                period_fin_states =curent_finace_states(start_data, ending_data,cur,taxes_system)

            return render(request, 'users/fin_states.html',
                                    {'start_data':start_data,
                                    'ending_data':ending_data,
                                    'period_fin_states':str(period_fin_states[0]),
                                    'tax_system':period_fin_states[1]})   

        conn.commit()
        conn.close()  

        fin_states = TimePeriodForm()
 
        return render(request, 'users/user_profile.html',
                                {'all_pp_buyers':all_pp_buyers,
                                'all_buyers_docs':all_buyers_docs,
                                'all_pp_providers':all_pp_providers,
                                'all_providers_docs':all_providers_docs,
                                'month_fin_states':month_fin_states[0],
                                'square_fin_states':square_fin_states[0],
                                'fin_states':fin_states,
                                'tax_system':month_fin_states[1],
                                'providers_debts':providers_debts,
                                'providers_prepay':providers_prepay,
                                'buyers_debts':buyers_debts,
                                'buyers_prepay':buyers_prepay,

                                'providers_debts_result':providers_debts_result,
                                'providers_prepay_result':providers_prepay_result,
                                'buyers_debts_result':buyers_debts_result,
                                'buyers_prepay_result':buyers_prepay_result,

                                })
    else:
         return HttpResponseRedirect("/")


#!----------https://djbook.ru/ch07s02.html,    
def show_sverka(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:

        conn = sqlite3.connect(str(user.id)+'.sqlite')
        cur = conn.cursor()

        if request.method == 'POST':
            sverka_form = ActSverkiForm(request.POST)     
            if sverka_form.is_valid():
                
                contragent_name = str(sverka_form.cleaned_data['name'])
                start_data = str(sverka_form.cleaned_data['start_date'])
                ending_data = str(sverka_form.cleaned_data['end_date'])
                
                resultaty = get_sverka(cur,contragent_name,start_data,ending_data)
                resultaty_past = get_sverka(cur,contragent_name,'2016-06-30',start_data)
                past_result = resultaty_past[3]

                contr_name = resultaty[0]
                outer_summ = resultaty[1]
                inner_summ = resultaty[2]
                result = resultaty[3]
                inner_docs_list = np.array(resultaty[4])
                outer_docs_list = np.array(resultaty[5])
                print(type(outer_docs_list),type(inner_docs_list))
                
                return render(request, 'users/act_sverki/sverka_result.html',
                                                    {'all_pp':outer_docs_list,
                                                    'all_tn':inner_docs_list,
                                                    'contr_name':contr_name,
                                                    'start_data':start_data,
                                                    'ending_data':ending_data,
                                                    'summa_sverki':result,
                                                    'inner_summ':inner_summ,
                                                    'outer_summ':outer_summ,
                                                    'past_result':past_result })

        sverka_form = ActSverkiForm()

        conn.commit()
        conn.close()  

        return render(request, 'users/act_sverki/akt_sverki.html',{'forma': sverka_form})
    else:
         return HttpResponseRedirect("/")   



def show_hvosty(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:

        conn = sqlite3.connect(str(user.id)+'.sqlite')
        cur = conn.cursor()

        if request.method == 'POST':
            hvosty_forma = TimePeriodForm(request.POST)     
            if hvosty_forma.is_valid():
          
                start_data = str(hvosty_forma.cleaned_data['start_date'])
                ending_data = str(hvosty_forma.cleaned_data['end_date'])
                
                providers_debts = get_hvosty_lists(cur,start_data,ending_data)[0]
                providers_prepay = get_hvosty_lists(cur,start_data,ending_data)[1]
                buyers_debts = get_hvosty_lists(cur,start_data,ending_data)[2]
                buyers_prepay = get_hvosty_lists(cur,start_data,ending_data)[3]
                
            return render(request, 'users/hvosty/hvosty_result.html',
                                    {'providers_debts':providers_debts,
                                    'providers_prepay':providers_prepay,
                                    'buyers_debts':buyers_debts, 
                                    'buyers_prepay':buyers_prepay, 
                                    'start_data':start_data,
                                    'ending_data':ending_data })   

        hvosty_forma = TimePeriodForm()

        conn.commit()
        conn.close()  


    return render(request, 'users/hvosty/hvosty.html',{'hvosty_forma':hvosty_forma})
    pass





