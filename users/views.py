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



def UsersList(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users':users})
    pass



def show_user_profile(request,id, **kwargs):
    user = get_object_or_404(User, id=id)
    if user == request.user:
        
        base_name = str(user.id)+'.sqlite'
        conn = sqlite3.connect(base_name)
        cur = conn.cursor()

        paginator = Paginator(create_list_of_table_values(cur.execute(select_all_documents),cur.description),15)

        all_documents = get_pages(request,paginator)

        conn.commit()
        conn.close()
   
        return render(request, 'users/user_profile.html',
        {'all_documents':all_documents})
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

                select_pp = select_docs.format(pp, str(order.contragent_id), "'"+start_data+"'", "'"+ending_data+"'")
                select_tn = select_docs.format(tn, str(order.contragent_id), "'"+start_data+"'", "'"+ending_data+"'")

                contragents_list = [2,5, 6,7,8,9,10, 11,12,13,16,"'     I'"]
                gg_hf = create_list_of_table_values(cur.execute(select_contragents_identificator),cur.description)
                archi = [nrm['parent'] for nrm in gg_hf]
                print(archi)


                credance = []
                for altair in archi:
                    select_tn2 = select_docs.format(tn, "'"+str(altair)+"'", "'"+start_data+"'", "'"+ending_data+"'")
                    select_pp2 = select_docs.format(pp, "'"+str(altair)+"'", "'"+start_data+"'", "'"+ending_data+"'")
                    all_pp2 = create_list_of_table_values(cur.execute(select_pp2),cur.description)
                    all_tn2 = create_list_of_table_values(cur.execute(select_tn2),cur.description)
                    summa_sverki = get_pays_balance(all_pp2, all_tn2, 'summ')
                    contr_name2 = all_tn2[0]['full_name']
                    print(summa_sverki)
                    print (contr_name2)   

   
                all_pp = create_list_of_table_values(cur.execute(select_pp),cur.description)
                all_tn = create_list_of_table_values(cur.execute(select_tn),cur.description)




                summa_sverki = get_pays_balance(all_pp, all_tn, 'summ')

 #               contr_name = all_tn[0]['full_name']

                contr_name = "ttt"
                return render(request, 'users/sverka_result.html',{'all_pp':all_pp,
                    'all_tn':all_tn,'contr_name':contr_name,'start_data':start_data,
                    'ending_data':ending_data,'summa_sverki':summa_sverki})

        forma = ContragentIdForm()
        return render(request, 'users/akt_sverki.html',{'forma': forma})
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

                select_pp = select_docs_for_data.format(pp, "'"+order.start_date+"'", "'"+order.end_date+"'")
                select_tn = select_docs_for_data.format(tn, "'"+order.start_date+"'", "'"+order.end_date+"'")

                all_pp = create_list_of_table_values(cur.execute(select_pp),cur.description)
                all_tn = create_list_of_table_values(cur.execute(select_tn),cur.description)

                sorted_pp = sorted(all_pp, key=lambda item: item['id'])
                sorted_tn = sorted(all_tn, key=lambda item: item['id'])

                nn = perebor(sorted_tn, 'id', 'doc_date', 'summ')
                mm = perebor(sorted_pp, 'id', 'doc_date', 'summ')
                print(nn)

                return render(request, 'users/hvosty_result.html',{'nn':nn, 'mm':mm,'sorted_pp':sorted_pp,'sorted_tn':sorted_tn })

        hvosty_forma = HvostyForm()    

    return render(request, 'users/hvosty.html',{'hvosty_forma':hvosty_forma})
    pass



def show_main_page(request):
    contacts = ContList.objects.all()

    if request.method == 'POST':
        form = ContactCreateForm(request.POST)
        new_name = Contact.first_name
        new_mail = Contact.address

        if form.is_valid():
            order = form.save()
            order.save()
 
            send_mail('Новый клиент', str(order.first_name),  from_who,
                to_me, fail_silently=False)

            return render(request, 'landing/thanks.html')
    form = ContactCreateForm()

    return render(request, 'landing/main.html',
    {'form': form,'contacts': contacts, 
    'temp':temp, 'desc':desc, 'icon':icon, 'mainDesc':mainDesc,
    'about':about, 'descript': descript, }) 

def show_contacts_page(request):

    return render(request, 'landing/contacts.html') 


