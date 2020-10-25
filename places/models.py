# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
from django.conf import settings


class Places(models.Model):
    amenity_choice = [('restaurant', 'restaurant'),
                      ('fast_food', 'fast food'),
                      ('cafe', 'cafe')]

    id = models.CharField(max_length=254, primary_key=True)
    amenity = models.CharField(max_length=254, choices=amenity_choice)
    name = models.CharField(max_length=254, null=True)
    website = models.CharField(max_length=254, null=True)
    cuisine = models.CharField(max_length=254, null=True)
    active = models.BooleanField(default=True)
    geom = models.PointField()

    def __str__(self):
        return self.name or "[Empty name]"


class Visit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='visits')
    date_visited = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.__str__()} {self.place.__str__()}"
