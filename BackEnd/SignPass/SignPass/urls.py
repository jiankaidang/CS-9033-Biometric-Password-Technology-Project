from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^signpass/service/checkBinding/$','sign.views.checkBinding'), 
    url(r'^signpass/service$','sign.views.index'), 
    url(r'^signpass/(?P<username>[^/]+)/bind$','sign.views.bind'),  
    url(r'^signpass/ios/(?P<username>[^/]+)/login/$','sign.views.login'),                 
    url(r'^signpass/ios/(?P<username>[^/]+)/register/$','sign.views.register'), 

  # Examples:
  # url(r'^$', 'SignPass.views.home', name='home'),
  # url(r'^SignPass/', include('SignPass.foo.urls')),

  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

  # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
