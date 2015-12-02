# -*- coding: utf-8 -*-
from django import forms

class QuadraticForm(forms.Form):
    a = forms.FloatField(label='коэффициент a', widget=forms.TextInput)
    b = forms.FloatField(label='коэффициент b', widget=forms.TextInput)
    c = forms.FloatField(label='коэффициент c', widget=forms.TextInput)
    def clean_a(self):
	data = self.cleaned_data['a']
	if data == 0:
	    raise forms.ValidationError('коэффициент при первом слагаемом уравнения не может быть равным нулю')
	return self.cleaned_data['a']