__author__ = 'Rajee'
from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),            #Links to the views file and links
                       url(r'^about$', views.about, name='about'),        #each url pattern with the correct name function.
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),)



