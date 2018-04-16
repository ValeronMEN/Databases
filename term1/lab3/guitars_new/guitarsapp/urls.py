from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^guitars', views.guitars),
    url(r'^customers', views.customers),
    url(r'^bills', views.bills),
    url(r'^shops', views.shops),
    url(r'^output/$', views.output_xml),
    url(r'^input/$', views.input_xml),
    url(r'^transput/$', views.transport_xml),
    url(r'^add_element/$', views.add_bill),
    url(r'^delete_element/', views.delete_element),
    url(r'^events/', views.events),
    url(r'^triggers/', views.triggers),
    url(r'^procedures/', views.procedures),
    url(r'^$', views.index, name='index'),
]