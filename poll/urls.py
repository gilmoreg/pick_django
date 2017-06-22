from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<user>\w+)/$', views.poll, name='poll'),
    url(r'^poll/create$', views.create_poll, name='create_poll'),
]