from django.shortcuts import render, get_object_or_404, redirect
from courses.models import Course, Lesson
from students.models import Student
# Create your views here.

def index(request):
    return render(request, 'index.html', { 'courses': Course.objects.all()})

def contact(request):
    return render(request, 'contact.html')

def language(request):
    if request.session.has_key('lang'):
	if request.session['lang'] == '':
	    request.session['lang'] = 'aurabesh'
	else:
	    request.session['lang'] = ''
    else:
	request.session['lang'] = 'aurabesh'
    return redirect(request.META['HTTP_REFERER'])
    

