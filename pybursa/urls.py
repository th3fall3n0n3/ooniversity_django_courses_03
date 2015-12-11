from django.conf.urls import patterns, include, url
from django.contrib import admin
from pybursa import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pybursa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^polls/', include('polls.urls', namespace = "polls")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'quadratic/', include('quadratic.urls')),
    url(r'^$', views.index, name = "index"),
    url(r'^change_lang/$', views.language, name = "language"),
    url(r'contact/', views.contact, name = "contact"),
    url(r'students/', include('students.urls', namespace = "students")),
    url(r'courses/', include('courses.urls', namespace = "courses")),
    url(r'coaches/', include('coaches.urls', namespace = "coaches")),
    url(r'feedback/', include('feedbacks.urls', namespace = "feedbacks"))
)

admin.site.site_header = 'My Site'