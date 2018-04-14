#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth import authenticate, login


import sqlite3
import os

from singles.dif import create_hvosty_excel, download_excel_doc
from users.models import *
from users.forms import *
from users import base_update as upd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"


    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")



def show_user_profile(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        base_name = BASE_DIR+'\\'+str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()
        taxes_system = user.client.nalog_system

        income_nds_month = curent_finace_states(start_month, var.today, cur, taxes_system)[2]
        outcome_nds_month = curent_finace_states(start_month, var.today, cur, taxes_system)[3]
        result_nds_month = curent_finace_states(start_month, var.today, cur, taxes_system)[0]


        income_nds_square = curent_finace_states(start_square, var.today, cur, taxes_system)[2]
        outcome_nds_square = curent_finace_states(start_square, var.today, cur, taxes_system)[3]
        result_nds_square = curent_finace_states(start_square, var.today, cur, taxes_system)[0]


        all_pp_buyers = get_paginator(cur, 'contragents_documents_two',sq_c.pp_buyers,15,request)
        all_buyers_docs = get_paginator(cur, 'contragents_documents_two',sq_c.tn_buyers,15,request)
        all_pp_providers = get_paginator(cur, 'contragents_documents',sq_c.pp_providers,15,request)
        all_providers_docs = get_paginator(cur, 'contragents_documents',sq_c.tn_providers,15,request)

        
        hvosty_list = get_hvosty_lists(cur,'2016-06-30',str(var.today))

        providers_debts = hvosty_list[0]
        providers_prepay = hvosty_list[1]
        buyers_debts = hvosty_list[2]
        buyers_prepay = hvosty_list[3]
    
        providers_debts_result = hvosty_list[4]
        providers_prepay_result = hvosty_list[5]
        buyers_debts_result = hvosty_list[6]
        buyers_prepay_result = hvosty_list[7]


        conn.commit()
        conn.close() 

        if request.method == 'POST':
            fin_states = TimePeriodForm(request.POST)     
            if fin_states.is_valid():
                download_excel_doc(request, create_hvosty_excel(request, buyers_prepay_result))

        fin_states = TimePeriodForm()
 
        return render(request, 'users/user_profile.html',
                                {'all_pp_buyers':all_pp_buyers,
                                'all_buyers_docs':all_buyers_docs,
                                'all_pp_providers':all_pp_providers,
                                'all_providers_docs':all_providers_docs,

                                'income_nds_month' :income_nds_month,
                                'outcome_nds_month': outcome_nds_month,
                                'result_nds_month': result_nds_month,

                                'income_nds_square': income_nds_square,
                                'outcome_nds_square': outcome_nds_square,
                                'result_nds_square': result_nds_square,

                                'tax_system':taxes_system,
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


def update_bases(request):
    for i in range(len(upd.bazi)):
        upd.full_update(i,i+1)
        
    return HttpResponseRedirect("/")








