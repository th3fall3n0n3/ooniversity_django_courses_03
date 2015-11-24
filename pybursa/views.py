from django.shortcuts import render, get_object_or_404
from courses.models import Course, Lesson
from students.models import Student
# Create your views here.

def index(request):
    return render(request, 'index.html', { 'courses': Course.objects.all()})

def contact(request):
    return render(request, 'contact.html')

