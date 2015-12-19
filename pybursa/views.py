from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from courses.models import Course, Lesson
from students.models import Student
from django.template import RequestContext

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
    

def not_found(request):
    response = render_to_response('errors/404.html', { 'message' : 'Sorry, page is not found' },
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def server_error(request):
    response = render_to_response('errors/500.html', { 'message' : 'Sorry, internal server error occurred' },
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response