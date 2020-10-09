from django.contrib.gis import admin
from .models import Places, Visit

admin.site.register(Places, admin.OSMGeoAdmin)

admin.site.register(Visit)
