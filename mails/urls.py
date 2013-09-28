from django.conf.urls import patterns, include, url


from .views import home,index

urlpatterns = patterns('',
    url(r"^home/$", home, name="home"),
)

