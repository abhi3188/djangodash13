from django.conf.urls import patterns, include, url
from django.contrib import admin

from mails.views import home

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mily.views.home', name='home'),
    # url(r'^mily/', include('mily.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
<<<<<<< HEAD

    url(r'^accounts/',include('allauth.urls')),
=======
>>>>>>> 7a679fee205d25fc5bb235e030bb791d37c3831f
    url(r'^$', index, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mails/', include('mails.urls', namespace="mails")),
    url(r'^documents/', include('documents.urls', namespace="documents")),
    url(r'^contacts/', include('contacts.urls', namespace="contacts")),
)
