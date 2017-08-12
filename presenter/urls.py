from django.conf.urls import url
from . import views

app_name = 'presenter'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^live/$', views.golive_viewer, name='golive_viewer'),
    url(r'^onair/$', views.onair, name='onair'),
    url(r'^stoplive/$', views.stoplive, name='stoplive'),
    url(r'^getdata/$', views.SlideData.as_view(), name='slidedata'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^(?P<presentation_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_presentation/$', views.create_presentation, name='create_presentation'),
    url(r'^(?P<presentation_id>[0-9]+)/create_slide/$', views.create_slide, name='create_slide'),
    url(r'^(?P<presentation_id>[0-9]+)/delete_slide/(?P<slide_id>[0-9]+)/$', views.delete_slide, name='delete_slide'),
    url(r'^(?P<presentation_id>[0-9]+)/delete_presentation/$', views.delete_presentation, name='delete_presentation'),
    url(r'^(?P<presentation_id>[0-9]+)/golive/$', views.golive, name='golive'),
    url(r'^pdf/present$', views.pdfjs_present, name='pdfjs_present'),
    # url(r'^view$', views.pdfjs_view, name='pdfjs_view'),
]

