from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^map$', views.map, name='map'),
    # ex: /polls/5/
    url(r'^(?P<attack_id>[0-9]+)/$', views.detail, name='detail'),
]