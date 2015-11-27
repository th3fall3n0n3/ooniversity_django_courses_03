from django.shortcuts import render
from courses.models import Course, Lesson

# Create your views here.
def detail(request, request_id):
    return render(request, 'courses/detail.html', { 'course' : Course.objects.get(id = request_id), 'lessons' : Lesson.objects.filter(course = request_id)})
