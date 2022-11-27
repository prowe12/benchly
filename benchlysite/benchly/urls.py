"""
benchly app URL Configuration
"""
from django.urls import path

# imported views
from . import views

urlpatterns = [
    # index: /benchly/
    path('', views.index, name='index'),
    # display: /benchly/3/atmos_co2/1/2022
    # path('<str:climvar>', views.index, name='index'),
]
