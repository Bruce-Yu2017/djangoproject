from django.conf.urls import url
import views

urlpatterns = [
  url(r'^$', views.index),
  url(r'regi$', views.register),
  url(r'login$', views.login), 
  url(r'travel$', views.travel),
  url(r'travel/add$', views.addplan),
  url(r'addtrip$', views.addtrip),
  url(r'destination/(?P<usertrip_id>\d+)$', views.showtrip), 
  url(r'join/(?P<joiner_id>\d+)$', views.join), 
  url(r'^$', views.logout)

]









