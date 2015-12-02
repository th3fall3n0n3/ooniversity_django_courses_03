# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from quadratic.forms import QuadraticForm

def quadratic_results(request):
    context={}
    if request.method == "GET" and request.GET.get('a') != None and request.GET.get('b') != None and request.GET.get('b') != None:
	context['form'] = QuadraticForm(request.GET)
	if context['form'].is_valid():
	    a = context['form'].cleaned_data['a']
	    b = context['form'].cleaned_data['b']
	    c = context['form'].cleaned_data['c']
	    # claculating discriminant
	    context['d'] = d = int(b ** 2 - 4 * a * c)
	    if d < 0:
		context['result'] = "Дискриминант меньше нуля, квадратное уравнение не имеет действительных решений."
	    elif d == 0:
		context['result'] = "Дискриминант равен нулю, квадратное уравнение имеет один действительный корень: x1 = x2 = %0.1f" % (-b / 2 * a)
	    else:
		x1 = (-b + d ** (1/2.0)) / (2 * a)
		x2 = (-b - d ** (1/2.0)) / (2 * a)
		context['result'] = "Квадратное уравнение имеет два действительных корня: x1 = %0.1f, x2 = %0.1f" % (x1, x2)
    else:
	context['form'] = QuadraticForm()
    return render(request, "quadratic/results.html",  context )
