from django.urls import path
from django.conf.urls import include, url
from . import views

# app_name = 'blueprint'

urlpatterns = [
    path('', views.main, name="index"),
    path('about', views.about, name="about"),
    path('catalog', views.catalog, name="catalog"),
    path('subscribe', views.subscription, name='subscribe'),
    path('letters', views.letters, name='letters'),
    path('contact', views.contact, name='contact'),
    path('clients', views.clients, name='clients'),
    path('more_gallery/<str:project_slug>', views.more_gallery, name='more_gallery'),
    path('unsubscribe/<str:email>', views.unsubscribe, name='unsubscribe'),
    path('project/<str:slug>', views.project, name='project'),
    path('service/<str:slug>', views.service, name='service'),
]