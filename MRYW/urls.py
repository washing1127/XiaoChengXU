from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from MRYW import views

urlpatterns = [
    url(r'index/', views.index),
    url(r'save/', views.create),
    url(r'login/', views.login),
]
