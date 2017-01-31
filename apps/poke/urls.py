from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^pokes$', views.dash),
    url(r'^logout$', views.log_out),
    url(r'^createpoke/(?P<id>\d+)$', views.create_poke)
]
