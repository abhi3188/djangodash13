from django.conf.urls import patterns, include, url
from django.contrib import admin

from mails.views import home, auth_return

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mily.views.home', name='home'),
    # url(r'^mily/', include('mily.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^accounts/',include('allauth.urls')),
    url(r'^$', home, name="home"),
    url(r'^oauth2callback$', auth_return,name="oauth2callback"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mails/', include('mails.urls', namespace="mails")),
    url(r'^documents/', include('documents.urls', namespace="documents")),
    url(r'^contacts/', include('contacts.urls', namespace="contacts")),
)
