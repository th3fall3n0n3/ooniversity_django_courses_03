from django.conf.urls import patterns, include, url
from django.contrib import admin
from courses import views

urlpatterns = patterns('',
    url(r'^(?P<request_id>[0-9]+)/$', views.detail, name = "detail"),
    url(r'^add/$', views.add, name = "add"),
    url(r'^edit/(?P<course_id>[0-9]+)/$', views.edit, name = "edit"),
    url(r'^remove/(?P<course_id>[0-9]+)/$', views.remove, name = "remove"),
    url(r'^(?P<course_id>[0-9]+)/add_lesson/$', views.add_lesson, name = "add-lesson")
)
