__author__ = 'Jiankai Dang'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'banksite.views.login_page'),
    url(r'^login_check', 'banksite.views.login_check'),
    url(r'^account', 'banksite.views.account'),
)