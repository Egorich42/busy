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
        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")



def show_user_profile(request,id, **kwargs):
    user = get_object_or_404(User, id=id)

    if user == request.user:
    
        base_name = str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()


        contragent_id = 17
        pp ="contragents_documents.summm != '0'"
        tn = "contragents_documents.summm = '0'"
        select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} ORDER BY contragents_documents.doc_date;"
        select_contragents_info="SELECT * FROM contragents LEFT JOIN contragents_places ON contragents.ID=contragents_places.m LEFT JOIN contragents_bank ON contragents.ID=contragents_bank.schet ;"
        select_all_documents="SELECT * FROM contragents_documents;"
        select_tn = select_docs.format(tn, contragent_id)   
        select_pp = select_docs.format(pp, contragent_id)



        def list_of_table_values(request_text):
            request_name = cur.execute(request_text).fetchall()
            list_to_sort = [list(elem) for elem in request_name]
            cols = [column[0] for column in cur.description]
            result = []
            for row in list_to_sort:
                result += [{col.lower():value for col,value in zip(cols,row)}]
            return result
            pass    

        def test_akt_sverki(request_text):
            request_name_akt = cur.execute(request_text).fetchall()
            list_to_sort = [list(elem) for elem in request_name_akt]
            cols = [column[0] for column in cur.description]
            resultat = []
            for row in list_to_sort:
                resultat += [{col.lower():value for col,value in zip(cols,row)}]
            return resultat
            pass 

                   
        all_documents = list_of_table_values(select_all_documents)
        contragents_list = list_of_table_values(select_contragents_info)
        all_pp = test_akt_sverki(select_pp)
        all_tn = test_akt_sverki(select_tn)


        pp_summ_list = [f[key] for key in['summ'] for f in all_pp]
        tn_summ_list = [f[key] for key in['summ'] for f in all_tn]
        pp_sum = sum(pp_summ_list)
        tn_sum = sum(tn_summ_list)

        


        conn.commit()
        conn.close()
   
        return render(request, 'users/user_profile.html',
        {'all_documents':all_documents, 'contragents_list':contragents_list,'all_pp':all_pp, 'all_tn':all_tn})
    else:
         return HttpResponseRedirect("/")   


def UsersList(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users':users})
    pass




