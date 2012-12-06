from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^signpass/service/checkBinding/$','sign.views.checkBinding'), 
    url(r'^signpass/service/bind$','sign.views.bind',name='bindRequest'),
    url(r'^signpass/service$','sign.views.index'), 
    url(r'^signpass/ios/(?P<username>[^/]+)/check_username/$','sign.views.checkUsername'),
    url(r'^signpass/(?P<service_name>[^/]+)/(?P<service_uid>[^/]+)/bind$','sign.views.bindRequestFromBank'),    
    url(r'^signpass/ios/(?P<username>[^/]+)/login/$','sign.views.login'),                 
    url(r'^signpass/ios/register/$','sign.views.register'), 
    url(r'^signpass/ios/verify/$','sign.views.verifySign'), 
    url(r'^signpass/ios/modify/$','sign.views.modifySign'),
    url(r'^signpass/ios/register_pushnotif$', 'sign.views.register_pushnotif'),
    url(r'^signpass/send_notification$', 'sign.views.send_notification'),


  # Examples:
  # url(r'^$', 'SignPass.views.home', name='home'),
  # url(r'^SignPass/', include('SignPass.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
