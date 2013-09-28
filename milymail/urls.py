from django.conf.urls import patterns, include, url

from milymail.views import home

urlpatterns = patterns('',
    
    url(r"^home/$", home, name="home"),    
    
)