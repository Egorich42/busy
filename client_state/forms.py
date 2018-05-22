#! /usr/bin/env python
# -*- coding: utf-8 -*
from django import forms
from .models import Upload_file
from django.forms import ModelForm

years = [("2018", "2018"),("2017", "2017"),("2016", "2016"), ("2015", "2015"),]


months = [ ("01", "январь", ),("02", "февраль", ),("03",  "март"),( "04","апрель"),("05", "май" ), ("06","июнь"),
			("07", "июль"),("08", "август"),("09", "сентябрь"), ("10", "октябрь"),("11", "ноябрь"),
			("12", "декабрь")]



days = [("01","01"), ("02","02"), ("03","03"), ("04","04"), ("05","05"), ("06","06"), ("07","07"), 
		("08","08"), ("09","09"), ("10","10"), ("11","11"), ("12","12"), ("13","13"),  
		("14","14"), ("15","15"), ("16","16"), ("17","17"), ("18","18"), ("19","19"),
		("20","20"), ("21","21"), ("22","22"), ("23","23"), ("24","24"), ("25","25"), 
		("26","26"),  ("27","27"),("28","28"), ("29","29"),  ("30","30"),  ("31", "31"), ]


class StateForm(forms.Form):	
	end_year = forms.ChoiceField(choices=years,widget=forms.Select)
	end_month = forms.ChoiceField(choices=months,widget=forms.Select)
	end_day = forms.ChoiceField(choices=days,widget=forms.Select)



class CurrStatForm(forms.Form):	
	start_year = forms.ChoiceField(choices=years,widget=forms.Select)
	start_month = forms.ChoiceField(choices=months,widget=forms.Select)
	start_day = forms.ChoiceField(choices=days,widget=forms.Select)

	end_year = forms.ChoiceField(choices=years,widget=forms.Select)
	end_month = forms.ChoiceField(choices=months,widget=forms.Select)
	end_day = forms.ChoiceField(choices=days,widget=forms.Select)


	
class TaxForm(forms.Form):

	start_year = forms.ChoiceField(choices=years,widget=forms.Select)
	start_month = forms.ChoiceField(choices=months,widget=forms.Select)
	start_day = forms.ChoiceField(choices=days,widget=forms.Select)


	end_year = forms.ChoiceField(choices=years,widget=forms.Select)
	end_month = forms.ChoiceField(choices=months,widget=forms.Select)
	end_day = forms.ChoiceField(choices=days,widget=forms.Select)

class FoundDifferenceForm(ModelForm):
  class Meta:
    model = Upload_file
    fields = ['uploaded_file', "start_year","start_month","start_day","end_year","end_month","end_day"]
