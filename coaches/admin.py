from django.contrib import admin
from coaches.models import Coach
# Register your models here.

class CoachAdmin(admin.ModelAdmin):
    list_display = [ 'get_name', 'get_last_name', 'gender', 'skype', 'description' ]
    list_filter = [ 'user__is_staff' ]
    
    def get_name(self, obj):
	return obj.user.first_name
    get_name.short_description = "Name"
    def get_last_name(self, obj):
	return obj.user.last_name
    get_last_name.short_description = "Last name"

admin.site.register(Coach, CoachAdmin)