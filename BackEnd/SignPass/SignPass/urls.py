from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^signpass/service/checkBinding$','sign.views.checkBinding'), 
    url(r'^signpass/service/bind$','sign.views.bind'),
    url(r'^signpass/service/bindRequestPoll$','sign.views.bindRequestPoll'),
    url(r'^signpass/service$','sign.views.index'), 
    url(r'^signpass/ios/(?P<username>[^/]+)/check_username/$','sign.views.checkUsername'),
    url(r'^signpass/(?P<service_name>[^/]+)/(?P<service_uid>[^/]+)/bindRequestFromService$','sign.views.bindRequestFromService'),    
    url(r'^signpass/ios/(?P<username>[^/]+)/login/$','sign.views.login'), 
    url(r'^signpass/ios/register/$','sign.views.register'), 
    url(r'^signpass/ios/verify/$','sign.views.verifySign'), 
    url(r'^signpass/ios/modify/$','sign.views.modifySign'), 
    url(r'^signpass/(?P<service_name>[^/]+)/(?P<service_uid>[^/]+)/serviceLogin$','sign.views.serviceLogin'),
    url(r'^signpass/send_notification$', 'sign.views.send_notification'),
    url(r'^signpass/service/loginRequestPoll$','sign.views.loginRequestPoll'),
    url(r'^signpass/service/serviceLoginRequest$','sign.views.serviceLoginRequest'),
    url(r'^signpass/ios/register_pushnotif$', 'sign.views.requestFromIOS'),
    # Examples:
  # url(r'^$', 'SignPass.views.home', name='home'),
  # url(r'^SignPass/', include('SignPass.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
