from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'loginproject.views.home', name='home'),
    url(r'^login/$', 'djangologinapp.views.login_app', name='login_app'),
	url(r'^signup/$', 'djangologinapp.views.signup_app', name='signup_app'),
	url(r'^logout/$', 'djangologinapp.views.logout_app', name='logout_app'),
	url(r'^getGData/$', 'djangologinapp.views.get_gdata', name='get_gdata'),
    #url(r'^admin/', include(admin.site.urls)),
)
