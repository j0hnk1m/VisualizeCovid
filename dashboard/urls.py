from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('fetch_dates/', views.fetch_dates, name='fetch_dates'),
]
