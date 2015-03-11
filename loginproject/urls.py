from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
print 

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sampleapp.views.home', name='home'),
    url(r'^' + settings.APP_URL_DOMAIN[1:], include('djangologinapp.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
