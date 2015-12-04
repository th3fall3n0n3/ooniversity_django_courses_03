from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Course, Lesson
from courses.forms import CourseModelForm, LessonModelForm

# Create your views here.
def detail(request, request_id):
    return render(request, 'courses/detail.html', { 'course' : Course.objects.get(id = request_id), 'lessons' : Lesson.objects.filter(course = request_id)})

def add(request):
    context = {}
    if request.POST:
	form = CourseModelForm(request.POST)
        if form.is_valid():
    	    data = form.cleaned_data
            form.save()
            messages.success(request, 'Course %s been successfully added.' % (data['name']))
            return redirect('index')
    else:
        form = CourseModelForm()
    return render(request, 'courses/add.html', { 'form' : form })

def edit(request, course_id):
        course = Course.objects.get(id=course_id)
        form = CourseModelForm(instance = course)
        if request.POST:
            form = CourseModelForm(request.POST, instance = course)
            if form.is_valid():
                form.save()
                messages.success(request, 'The changes have been saved.')
		return redirect('courses:detail',  course.id)
        return render(request, 'courses/edit.html', { 'form' : form } )

def remove(request, course_id):
        course = Course.objects.get(id = course_id)
        if request.POST:
            course.delete()
            messages.success(request, "Course %s has been deleted." % (course.name))
            return redirect('index')
        return render(request, 'courses/remove.html', { 'course' : course })

def add_lesson(request, course_id):
    context = {}
    if request.POST:
        form = form = LessonModelForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            messages.success(request, 'Lesson %s has been successfully added.' % (data['subject']))
            return redirect('courses:detail', data['course'].id)
        else:
            messages.warning(request, 'Warning, wrong data in the form.')
    else:
        form = LessonModelForm(initial={ 'course' : course_id })
    return render(request, 'courses/add_lesson.html', { 'form': form })
