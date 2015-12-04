from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Course, Lesson
from courses.forms import CourseModelForm, LessonModelForm

# Create your views here.
def detail(request, request_id):
    return render(request, 'courses/detail.html', { 'course' : Course.objects.get(id = request_id), 'lessons' : Lesson.objects.filter(course = request_id)})

def add(request):
    context = {}
    if request.method == "POST":
	context['form'] = form = CourseModelForm(request.POST)
        if form.is_valid():
    	    data = form.cleaned_data
            course = form.save()
            messages.success(request, 'Course %s been successfully added.' % (course.name))
            return redirect('index')
        else:
            messages.warning(request, 'Warning, wrong data in the form.')
    else:
        context['form'] = CourseModelForm()
    return render(request, 'courses/add.html', context)

def edit(request, course_id):
        course = Course.objects.get(id=course_id)
        if request.method == "GET":
            form = CourseModelForm(instance = course)
        elif request.method == "POST":
            form = CourseModelForm(request.POST, instance = course)
            if form.is_valid():
                course = form.save()
                messages.success(request, 'The changes have been saved.')
		return redirect('courses:detail',  course.id)
            else:
                messages.warning(request, 'Wrong data in the form, please correct.')
        return render(request, 'courses/edit.html', { 'form' : form } )

def remove(request, course_id):
        course = Course.objects.get(id = course_id)
        if request.method == "POST":
            course.delete()
            messages.success(request, "Course %s has been deleted." % (course.name))
            return redirect('index')
        return render(request, 'courses/remove.html', { 'course' : course })

def add_lesson(request, course_id):
    context = {}
    if request.method == "POST":
        context['form'] = form = LessonModelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            lesson = form.save()
            messages.success(request, 'Lesson %s has been successfully added.' % (lesson.subject))
            return redirect('courses:detail', lesson.course.id)
        else:
            messages.warning(request, 'Warning, wrong data in the form.')
    else:
        context['form'] = LessonModelForm(initial={ 'course' : course_id })
    return render(request, 'courses/add_lesson.html', context)
