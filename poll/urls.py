from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>\w+)/$', views.poll, name='poll'),
    url(r'^(?P<username>\w+)/vote$', views.vote, name='poll'),
    url(r'^(?P<username>\w+)/result$', views.result, name='poll'),
    url(r'^poll/create$', views.create_poll, name='create_poll'),
]