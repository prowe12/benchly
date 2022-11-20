"""
benchly app URL Configuration
"""
from django.urls import path

# imported views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
