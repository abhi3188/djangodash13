from django.conf.urls import patterns, include, url


from .views import home,index, sign_in, inbox, compose, attachments

urlpatterns = patterns('',
    url(r"^home/$", home, name="home"),
    url(r"^sign_in/$", sign_in),
    url(r"^inbox/$", inbox),
    url(r"^compose/(?P<provider_id>\w+)?$", compose,name="compose"),
    url(r"^attachments/$", attachments),
)

