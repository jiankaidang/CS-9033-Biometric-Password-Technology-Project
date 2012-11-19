__author__ = 'Jiankai Dang'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'banksite.views.home', name='home'),
    url(r'^login/$', 'banksite.views.login'),
)