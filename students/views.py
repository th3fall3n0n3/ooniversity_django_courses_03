from django.shortcuts import render
from students.models import Student

# Create your views here.
def list_view(request):
    if request.GET.get('course_id'):
	students=Student.objects.filter(courses=request.GET.get('course_id'))
    else:
	students=Student.objects.all()
    return render(request, 'students/list_view.html', {'students': students})    

def detail(request, student_id):
    return render(request, 'students/detail.html', { 'student' : Student.objects.get(id=student_id)})
