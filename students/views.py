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
	if request.POST:
	    form = StudentModelForm(request.POST)
	    if form.is_valid():
		form.save()
		data = form.cleaned_data
		messages.success(request, 'Student %s %s has been successfully added.' % (data['name'], data['surname']))
		return redirect('students:list_view')
	else:
	    form = StudentModelForm()
	return render(request, 'students/add.html', { 'form' : form })

def edit(request, student_id):
	student = Student.objects.get(id = student_id)
	if request.POST:
	    form = StudentModelForm(request.POST, instance = student)
	    if form.is_valid():
		form.save()
		messages.success(request, 'Info on the student has been sucessfully changed.')
	else:
	    form = StudentModelForm(instance = student)
	return render(request, 'students/edit.html', { 'form' : form } )

def remove(request, student_id):
	student = Student.objects.get(id = student_id)
	if request.method == "POST":
	    student.delete()
	    messages.success(request, "Info on %s %s has been sucessfully deleted." % (student.name, student.surname))
	    return redirect('students:list_view')
	return render(request, 'students/remove.html', { 'student' : student })