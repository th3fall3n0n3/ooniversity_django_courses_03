from django.conf.urls import patterns, include, url
from django.contrib import admin
from students import views

urlpatterns = patterns('',
	url(r'^$', views.list_view, name = "list_view"),
	url(r'(?P<student_id>[0-9]+)/$', views.detail, name = "detail" )
)