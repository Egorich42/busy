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

        square_fin_states =curent_finace_states(start_square, today,cur)
        month_fin_states = curent_finace_states(start_month ,today,cur)

        if user.client.nalog_system == 'НДС':
            month_fin_states = month_fin_states[0]
            square_fin_states = square_fin_states[0]
            tax_system = "НДС" 
        else:
            month_fin_states = month_fin_states[1]
            square_fin_states = square_fin_states[1] 
            tax_system = "УСН"           
            pass
        paginator = Paginator(create_list_of_table_values(cur.execute(select_all_documents),cur.description),15)

        all_documents = get_pages(request,paginator)


        if request.method == 'POST':
            fin_states = FinStatesForm(request.POST)     
            if fin_states.is_valid():
                order = fin_states.save()
                order.save()
          
                start_data = order.start_date
                ending_data = order.end_date

                period_fin_states =curent_finace_states(start_data, ending_data,cur)

                if user.client.nalog_system == 'ндс.' or 'НДС':
                    period_fin_states = period_fin_states[0]
                    tax_system = "НДС" 

                else:
                    period_fin_states = period_fin_states[1]
                    tax_system = "УСН" 


            return render(request, 'users/fin_states.html',
                {'start_data':start_data,'ending_data':ending_data,'period_fin_states':str(period_fin_states),'tax_system':tax_system})   

        conn.commit()
        conn.close()  

        fin_states = FinStatesForm()
 
        return render(request, 'users/user_profile.html',
        {'all_documents':all_documents, 'month_fin_states':month_fin_states,
          'square_fin_states':square_fin_states,'fin_states':fin_states,'tax_system':tax_system})
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

                select_docs = [select_docs.format(doc, "'"+str(order.contragent_id)+"'", "'"+start_data+"'", "'"+ending_data+"'") for doc in (pp,tn)]

                all_pp_and_tn = [create_list_of_table_values(cur.execute(doc),cur.description) for doc in (select_docs)]

                summa_sverki = get_pays_balance(all_pp_and_tn[0], all_pp_and_tn[1], 'summ')

                contr_name = all_tn[0]['name']
                
                return render(request, 'users/sverka_result.html',{'all_pp':all_pp_and_tn[0],
                    'all_tn':all_pp_and_tn[1],'contr_name':contr_name,'start_data':start_data,
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
          
                gg_hf = create_list_of_table_values(cur.execute(select_contragents_identificator),cur.description)
                names = []
                names2=[]

                archi = [nrm['id'] for nrm in gg_hf]

                start_data = order.start_date
                ending_data = order.end_date

                for altair in archi:
                    select_documents = [select_docs_two.format(doc, "'"+str(altair)+"'", "'"+start_data+"'","'"+ending_data+"'") for doc in (tn2,pp2)]
                    select_documents2 = [select_docs.format(doc2, "'"+str(altair)+"'", "'"+start_data+"'","'"+ending_data+"'") for doc2 in (tn,pp)]
                    

                    all_docs = [create_list_of_table_values(cur.execute(table),cur.description) for table in select_documents]
                    all_docs2 = [create_list_of_table_values(cur.execute(table2),cur.description) for table2 in select_documents2]

                    summa_sverki = get_pays_balance(all_docs[1], all_docs[0], 'summ')
                    summa_sverkii = get_pays_balance(all_docs2[1], all_docs2[0], 'summ')


                    if summa_sverki !='OK!' and len(all_docs[0])>0:
                        names += [{'name':all_docs[0][0]['name'], 'summa':summa_sverki}]
                        pass

                    if summa_sverkii !='OK!' and len(all_docs2[0])>0:
                        names2 += [{'name':all_docs2[0][0]['name'], 'summa2':summa_sverkii}]
                        pass  

      
                
            return render(request, 'users/hvosty_result.html',
                {'names':names,'names2':names2,'start_data':start_data,'ending_data':ending_data })   

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


