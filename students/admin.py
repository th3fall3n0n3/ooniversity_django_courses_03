from django.contrib import admin
from students.models import Student

class StudentAdmin(admin.ModelAdmin):
    search_fields = [ 'surname', 'email' ]
    list_display = [ 'get_full_name', 'email', 'skype' ]
    list_filter = [ 'courses' ]
    fieldsets = [ ('Personal info', { 'fields' : [ 'name', 'surname', 'date_of_birth' ]} ),
		  ('Contact info', { 'fields' : [ 'email', 'phone', 'address' , 'skype']} ), 
		  ( None, { 'fields' : [ 'courses' ]} )
		]
    filter_horizontal = [ 'courses' ] 

    def get_full_name(self, obj):
	return obj.name+" "+obj.surname
    get_full_name.short_description = "Full name"
    get_full_name.admin_order_field = "name"
# Register your models here.

admin.site.register(Student, StudentAdmin)

