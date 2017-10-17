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
#https://djbook.ru/examples/39/
#https://ustimov.org/posts/17/
#http://acman.ru/django/publichnyi-profil-i-lichnyi-kabinet-po-odnoi-ssylk/
#python manage.py version


# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.


pp ="contragents_documents.summm != '0'"
tn = "contragents_documents.summm = '0'"
start_date = "'2014-09-02'"
end_date = "'2018-09-12'"
select_all_documents="SELECT * FROM contragents_documents;"
select_docs = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND contragents_documents.parent = {} AND  doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"
select_docs_for_data = "SELECT * FROM contragents_documents LEFT JOIN contragents ON contragents_documents.parent=contragents.id WHERE {} AND doc_date >= {} AND  doc_date <= {} ORDER BY contragents_documents.doc_date;"

def create_list_of_table_values(request_text, massive_from_table):
    request_name = request_text.fetchall()
    list_to_sort = [list(elem) for elem in request_name]
    cols = [column[0] for column in massive_from_table]
    result = []
    for row in list_to_sort:
        result += [{col.lower():value for col,value in zip(cols,row)}]
    return result
    pass 

def perebor(data_sorted, one, two, three):
    albert = []
    for key, group in itertools.groupby(data_sorted, key=lambda x:x[one]):
        a = list(sorted(group, key=lambda item: item[two]))
        suma = sum([f[key] for key in[three] for f in a])
        albert += [sum([f[key] for key in[three] for f in a])]
    
    return albert     

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

        all_documents = create_list_of_table_values(cur.execute(select_all_documents),cur.description)

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

                select_pp = select_docs.format(pp, str(order.contragent_id), order.start_date, order.end_date)
                select_tn = select_docs.format(tn, str(order.contragent_id), order.start_date, order.end_date)

                all_pp = create_list_of_table_values(cur.execute(select_pp),cur.description)
                all_tn = create_list_of_table_values(cur.execute(select_tn),cur.description)


               
                return render(request, 'users/sverka_result.html',{'all_pp':all_pp,'all_tn':all_tn})

        forma = ContragentIdForm()
        return render(request, 'users/akt_sverki.html',{'forma': forma})

    else:
         return HttpResponseRedirect("/")   




def UsersList(request):
    users = User.objects.all()

    return render(request, 'users/users_list.html', {'users':users})
    pass


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


                select_pp = select_docs_for_data.format(pp, order.start_date, order.end_date)
                select_tn = select_docs_for_data.format(tn, order.start_date, order.end_date)

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