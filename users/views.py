#! /usr/bin/env python
# -*- coding: utf-8 -*
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import  get_paginator
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

from client_state.models import Hvosty, CompanyBalance

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from forge import start_month, start_square, today


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

        if taxes_system == 'nds' or taxes_system == 'NDS':
            nds_month_res = CompanyBalance(base_name, "'"+start_month+"'", "'"+ str(today)+"'").count_nds()
            nds_square_res = CompanyBalance(base_name, "'"+start_square+"'", "'"+ str(today)+"'").count_nds()

            nds_month = [{"name": "Входной НДС", "value": str(round(nds_month_res[0],2))},
            {"name": "Исходящий НДС", "value":str(round(nds_month_res[1],2))},
            {"name": "НДС к уплате", "value":str(round(nds_month_res[2],2))}]

            nds_square =  [{"name":"Входной НДС", "value":str(round(nds_square_res[0],2))},
            {"name": "Исходящий НДС", "value":str(round(nds_square_res[1],2))},
            {"name":"НДС к уплате", "value":str(round(nds_square_res[2],2))}]
            usn_month = None
            usn_square = None

        else:
            usn_month = [{"name": "УСН за текущий месяц", "value": str(round(CompanyBalance(base_name, "'"+start_month+"'", "'"+ str(today)+"'").count_usn(),2))}]
            usn_square = [{"name": "УСН за текущий квартал", "value": str(round(CompanyBalance(base_name, "'"+start_square+"'", "'"+ str(today)+"'").count_usn(),2))}]
            nds_month = None
            nds_square = None

        all_pp_buyers = get_paginator(cur, 'contragents_documents_two',sq_c.pp_buyers,15,request)
        all_buyers_docs = get_paginator(cur, 'contragents_documents_two',sq_c.tn_buyers,15,request)
        all_pp_providers = get_paginator(cur, 'contragents_documents',sq_c.pp_providers,15,request)
        all_providers_docs = get_paginator(cur, 'contragents_documents',sq_c.tn_providers,15,request)


#        hvosty_list = Hvosty(base_name,"'"+ '2016-06-30'+"'", "'"+ str(var.today)+"'").show_contragent_balance()

#        providers_debts = hvosty_list[0]
#        providers_prepay = hvosty_list[1]
#        buyers_debts = hvosty_list[2]
#        buyers_prepay = hvosty_list[3]
    
 
        return render(request, 'users/user_profile.html',
                                {'all_pp_buyers':all_pp_buyers,
                                'all_buyers_docs':all_buyers_docs,
                                'all_pp_providers':all_pp_providers,
                                'all_providers_docs':all_providers_docs,

                                'tax_system':taxes_system,
#                                'providers_debts':providers_debts,
#                                'providers_prepay':providers_prepay,
#                                'buyers_debts':buyers_debts,
#                                'buyers_prepay':buyers_prepay,

                                "nds_month": nds_month,
                                "nds_square": nds_square,
                                "usn_month": usn_month,
                                "usn_square": usn_square, 

                                })
        pass



