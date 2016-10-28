from django.conf.urls import url

from . import views

# these urls are all messed up do this when more awake
urlpatterns = [
    url(r'^index$', views.index, name='index'),
    # url(r'^map$', views.map, name='map'),

     # url(r'^map/(?P<year>2[0-9]+)/$', views.year, name='year'),
    # ex: /polls/5/
    url(r'^(?P<attack_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'', views.map, name='map'),
]