"""
URL Configurations for the specific app
"""
from django.urls import path

# imported views
from . import views

# The urlpatterns map to the views.
# When <type:variable> is included in the URL path, the variable is sent
# as a keyword argument to the view function
app_name = 'my_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:scenario_id>/', views.results, name='results'),
]
