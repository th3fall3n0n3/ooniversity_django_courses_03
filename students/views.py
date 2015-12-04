from django.shortcuts import render, redirect
from students.models import Student
from students.forms import StudentModelForm
from courses.models import Course
from django.contrib import messages

# Create your views here.
def list_view(request):
    if request.GET.get('course_id'):
	students = Student.objects.filter(courses = request.GET.get('course_id'))
	return render(request, 'students/list.html', {'students': students, 'course_id' : request.GET.get('course_id') })
    else:
	students = Student.objects.all()
	return render(request, 'students/list.html', {'students': students})    

def detail(request, student_id):
    return render(request, 'students/detail.html', { 'student' : Student.objects.get(id = student_id)})

def create(request):
	context = {}
	if request.method == "POST":
	    context['form'] = form = StudentModelForm(request.POST)
	    if form.is_valid():
		data = form.cleaned_data
		student = form.save()
		messages.success(request, 'Student %s %s has been successfully added.' % (student.name, student.surname))
		return redirect('students:list_view')
	else:
	    context['form'] = StudentModelForm()
	return render(request, 'students/add.html', context )

def edit(request, student_id):
	student = Student.objects.get(id = student_id)
	if request.method == "GET":
	    form = StudentModelForm(instance = student)
	elif request.method == "POST":
	    form = StudentModelForm(request.POST, instance = student)
	    if form.is_valid():
		student = form.save()
		messages.success(request, 'Info on the student has been sucessfully changed.')
	return render(request, 'students/edit.html', { 'form' : form } )

def remove(request, student_id):
	student = Student.objects.get(id = student_id)
	if request.method == "POST":
	    student.delete()
	    messages.success(request, "Info on %s %s has been sucessfully deleted." % (student.name, student.surname))
	    return redirect('students:list_view')
	return render(request, 'students/remove.html', { 'student' : student })