__author__ = 'Jiankai Dang'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'banksite.views.login_page', name='login_page'),
    url(r'^login_check', 'banksite.views.login_check'),
    url(r'^login', 'banksite.views.login', name='login'),
    url(r'^accounts', 'banksite.views.accounts', name='accounts'),
    url(r'^logout', 'banksite.views.logout', name='logout'),
    url(r'^signpass_login', 'banksite.views.signpass_login'),
)