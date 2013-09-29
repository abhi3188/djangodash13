from django.conf.urls import patterns, include, url


from .views import home,index, sign_in, inbox, compose, attachments

urlpatterns = patterns('',
    url(r"^home/$", home, name="home"),
    url(r"^sign_in/$", sign_in),
    url(r"^inbox/(?P<provider_id>\w+/)?$", inbox, name="inbox"),
    url(r"^compose/(?P<provider_id>\w+)?$", compose, name="compose"),
    url(r"^attachments/(?P<provider_id>\w+)?$", attachments, name="attachments"),
)

