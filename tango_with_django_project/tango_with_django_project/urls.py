from django.conf.urls import patterns, include, url
from django.contrib import admin
from rango import urls
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),          # Reference the url pattern and passes it onto the url
    url(r'^rango/', include('rango.urls'))              # found in the Rango directory



   )
if settings.DEBUG:                                      #runs if dDEBUG is true in settings.py
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
