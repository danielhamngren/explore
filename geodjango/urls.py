"""geodjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.gis import admin
from django.urls import path

import places.views

urlpatterns = [
    path('time/', places.views.current_datetime),
    path('api/places', places.views.places),
    path('api/visits', places.views.visits),
    path('api/register_visit', places.views.register_visit),
    path('api/mapbox_token', places.views.mapbox_token),
    path('admin/', admin.site.urls),
    path('', places.views.index, name='index')
]
