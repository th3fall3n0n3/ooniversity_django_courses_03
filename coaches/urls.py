from django.conf.urls import patterns, include, url
from django.contrib import admin
from coaches import views

urlpatterns = patterns('',
	url(r'(?P<coach_id>[0-9]+)/$', views.detail, name = "detail" )
)