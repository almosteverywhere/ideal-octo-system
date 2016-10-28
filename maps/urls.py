from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^(?P<year_id>[0-9]+)/$', views.year, name='year'),
]