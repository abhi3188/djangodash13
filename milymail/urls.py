from django.conf.urls import patterns, include, url


from milymail.views import home,index

urlpatterns = patterns('',
    url(r"^$",index,name="index"),
    url(r"^home/$", home, name="home"),
)

