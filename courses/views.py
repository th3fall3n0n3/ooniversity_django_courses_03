import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from courses.models import Course, Lesson
from courses.forms import CourseModelForm, LessonModelForm

logger = logging.getLogger(__name__)

# Create your views here.
class CourseDetailView(DetailView):
    model = Course
    fields = '__all__'
    template_name = 'courses/detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
	logger.debug('Courses detail view has been debugged')
	logger.info('Logger of courses detail view informs you!')
	logger.warning('Logger of courses detail view warns you!')
	logger.error('Courses detail view went wrong!')
	context = super(CourseDetailView, self).get_context_data(**kwargs)
	context['lessons'] = Lesson.objects.filter(course=self.get_object().id)
	return context

class CourseCreateView(CreateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/add.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
	context = super(CourseCreateView, self).get_context_data(**kwargs)
	context['title'] = "Course creation"
	return context

    def form_valid(self, form):
	data = form.cleaned_data
	messages.success(self.request, 'Course %s has been successfully added.' % (data['name']))
	return super(CourseCreateView, self).form_valid(form)

class CourseUpdateView(UpdateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/edit.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
	context = super(CourseUpdateView, self).get_context_data(**kwargs)
	context['title'] = "Course update"
	return context

    def form_valid(self, form):
	data = form.instance
	messages.success(self.request, 'The changes have been saved.')
	self.success_url = reverse('courses:edit', args=(data.id,))
	return super(CourseUpdateView, self).form_valid(form)

class CourseDeleteView(DeleteView):
    model = Course
    fields = '_all__'
    template_name = 'courses/remove.html'
    context_object_name = 'course'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
	context = super(CourseDeleteView, self).get_context_data(**kwargs)
	context['title'] = "Course deletion"
	return context

    def delete(self, request, *args, **kwargs):
	course = self.get_object()
	messages.success(self.request, 'Course %s has been deleted.' % (course.name))
	return super(CourseDeleteView, self).delete(request, *args, **kwargs)

def add_lesson(request, course_id):
    if request.POST:
        form = LessonModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson %s has been successfully added.' % ( form.cleaned_data['subject']))
            return redirect('courses:detail', form.cleaned_data['course'].id)
    else:
        form = LessonModelForm(initial={ 'course' : course_id })
    return render(request, 'courses/add_lesson.html', { 'form' : form })
