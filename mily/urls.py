from django.conf.urls import patterns, include, url
from django.contrib import admin

from mails.views import index

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
    url(r'^$', index, name="home"),
>>>>>>> c7730245e220547facf9fee7325c41ae4304435e
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mails/', include('mails.urls', namespace="mails")),
    url(r'^documents/', include('documents.urls', namespace="documents")),
    url(r'^contacts/', include('contacts.urls', namespace="contacts")),
)
