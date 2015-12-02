# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from quadratic.forms import QuadraticForm

def quadratic_results(request):
    context={}
    if request.method == "GET" and request.GET.get('a') != None and request.GET.get('b') != None and request.GET.get('b') != None:
	form = QuadraticForm(request.GET)
	if form.is_valid():
	    a = form.cleaned_data['a']
	    b = form.cleaned_data['b']
	    c = form.cleaned_data['c']
	    # claculating discriminant
	    d = b ** 2 - 4 * a * c
	    if d < 0:
		result = "Дискриминант меньше нуля, квадратное уравнение не имеет действительных решений."
	    elif d == 0:
		result = "Дискриминант равен нулю, квадратное уравнение имеет один действительный корень: x1 = x2 = %0.1f" % (-b / 2 * a)
	    else:
		x1 = (-b + d ** (1/2.0)) / (2 * a)
		x2 = (-b - d ** (1/2.0)) / (2 * a)
		result = "Квадратное уравнение имеет два действительных корня: x1 = %0.1f, x2 = %0.1f" % (x1, x2)
	    context['d'] = d
	    context['result'] = result
	context['form'] = form
    else:
	context['form'] = QuadraticForm()
    return render(request, "quadratic/results.html",  context )
