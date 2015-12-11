from django.conf.urls import patterns, include, url
from django.contrib import admin
from feedbacks import views

urlpatterns = patterns('',
	url(r'^$', views.FeedbackView.as_view(), name = "feedback"),
)