"""benchly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# imported views
# from my_app import views

# The urlpatterns map to the views.
# When <type:variable> is included in the URL path, the variable is sent
# as a keyword argument to the view function
urlpatterns = [
    path('benchly/', include('benchly.urls')),
    path('admin/', admin.site.urls),
]
