import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from geodjango import settings

from places.models import Places, Visit


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"<html><body>It is now {now}.</body></html>"
    return HttpResponse(html)


def places(request):

    data = serializers.serialize('geojson', Places.objects.filter(amenity="cafe"))

    return HttpResponse(data, content_type='application/json')


def register_visit(request):
    # TODO: Handle errors and edge cases here
    if request.method == 'GET':
        place = Places.objects.get(id=request.GET["place"])
        visit = Visit(user=request.user, place=place)
        visit.save()

    return HttpResponse(request.__str__())


def mapbox_token(request):
    return HttpResponse(settings.MAPBOX_TOKEN)

def index(request):
    return render(request, 'index.html')
