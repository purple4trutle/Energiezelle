from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^index.html/', views.home, name='home'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^download_pdf/$', views.download_pdf, name='download_pdf'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^overview/$', views.overview, name='overview'),
    re_path(r'^buildingdata/$', views.buildingdata, name='buildingdata'),
    re_path(r'^add_year/$', views.add_year, name='add_year'),#calculation
    re_path(r'^calculation/$', views.calculation, name='calculation'),
    re_path(r'^calculation_admin/$', views.calculation_admin, name='calculation_admin'),
    re_path(r'^pdf_admin/$', views.pdf_admin, name='pdf_admin'),
    re_path(r'^impressum/$', views.impressum, name='impressum'),
    re_path(r'^datenschutz/$', views.datenschutz, name='datenschutz'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        views.activate, name='activate'),
]