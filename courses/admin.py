from django.contrib import admin
from courses.models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    fields = [ 'subject', 'description' , 'order' ]

class CourseAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'short_description' ]
    fields = [ 'name', 'short_description', 'description' ]
    search_fields = [ 'name' ]
    inlines = [ LessonInline ]

# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)


