#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import curent_finace_states, get_paginator, get_hvosty_lists, start_square, start_month
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
import sqlite3
from . import sql_commands as sq_c
from . import variables as var
from django.contrib.auth import authenticate, login
import os

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
    if request.user.username == "busy":
        clients = Client.objects.all()
        return render(request, "singles/clients/clients_list.html", {'clients':clients})

    if user == request.user:
        
        base_name = BASE_DIR+'\\'+'sqlite_bases'+'\\'+str(user.username)+'.sqlite'
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

        
        hvosty_list = get_hvosty_lists(cur, '2016-06-30', str(var.today))

        providers_debts = hvosty_list[0]
        providers_prepay = hvosty_list[1]
        buyers_debts = hvosty_list[2]
        buyers_prepay = hvosty_list[3]
    
        providers_debts_result = hvosty_list[4]
        providers_prepay_result = hvosty_list[5]
        buyers_debts_result = hvosty_list[6]
        buyers_prepay_result = hvosty_list[7]
 
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
        pass



