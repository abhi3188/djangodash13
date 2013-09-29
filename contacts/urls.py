from django.conf.urls import patterns, include, url
from contacts.views import all_contacts

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mily.views.home', name='home'),
    # url(r'^mily/', include('mily.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^all/',all_contacts,name='all_contacts'),
)