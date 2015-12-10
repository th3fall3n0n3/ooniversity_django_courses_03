from django.conf.urls import patterns, include, url
from django.contrib import admin
from students import views

urlpatterns = patterns('',
	url(r'^$', views.StudentListView.as_view(), name = "list_view"),
	url(r'^(?P<pk>[0-9]+)/$', views.StudentDetailView.as_view(), name = "detail" ),
	url(r'add/$', views.StudentCreateView.as_view() , name = "add" ),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.StudentUpdateView.as_view(), name = "edit"),
	url(r'^remove/(?P<pk>[0-9]+)/$', views.StudentDeleteView.as_view(), name = "remove")
)