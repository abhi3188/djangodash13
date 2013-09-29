from django.conf.urls import patterns, include, url


from .views import home,index, sign_in, inbox, compose, attachments, categorize,categorize_type

urlpatterns = patterns('',
    url(r"^home/$", home, name="home"),
    url(r"^sign_in/$", sign_in),
    url(r"^inbox/(?P<provider_id>\w+)?$", inbox, name="inbox"),
    url(r"^compose/(?P<provider_id>\w+)?$", compose),
    url(r"^attachments/(?P<provider_id>\w+)?$", attachments, name="attachments"),
    url(r"^categorize/$", categorize,name='categorize'),
    url(r"^categorize/(?P<id>\d+)/(?P<type>\d+)/$",categorize_type, name='categorize'),

)

