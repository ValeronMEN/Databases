from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^guitars', views.guitars),
    url(r'^customers', views.customers),
    url(r'^output/$', views.output_xml),
    url(r'^input/$', views.input_xml),
    url(r'^transput/$', views.transput_xml),
    url(r'^$', views.index, name='index'),
]