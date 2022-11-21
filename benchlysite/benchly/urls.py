"""
benchly app URL Configuration
"""
from django.urls import path

# imported views
from . import views

urlpatterns = [
    # index: /benchly/
    path('', views.index, name='index'),
    # detail: /benchly/5/
    path('<int:scenario>/', views.detail, name='detail'),
    # results: /benchly/5/results/
    path('<int:scenario>/<int:year>/results/', views.results, name='results'),
    # vote: /benchly/5/vote/
    path('<int:scenario>/vote/', views.vote, name='vote'),
]
#    path('<int:timeseries_scenario>/<int:disp_scenario>/', views.vote, name='vote'),
