import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from geodjango import settings

from places.models import Places, Visit
from django.db.models import F, Sum, Count, Case, When, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.views.decorators.cache import cache_page


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"<html><body>It is now {now}.</body></html>"
    return HttpResponse(html)


@cache_page(60 * 60 * 8)
def places(request):
    print(f"request user: {request.user}")

    # # Left join by Björn
    # qset = Places.objects.annotate(nbr_visits=Count(Case(When(visits__user=request.user, then=1)))).all()
    # data = serializers.serialize('geojson', qset)
    data = serializers.serialize('geojson', Places.objects.filter(active=True))
    return HttpResponse(data, content_type='application/json')


def visits(request):
    print(f"user is authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        qset = Visit.objects.filter(user=request.user)
        # print(qset)
        print(f'qset {qset}')
        data = serializers.serialize('json', qset)
    else:
        data = '{}'
    return HttpResponse(data, content_type='application/json')


def register_visit(request):
    # TODO: Handle errors and edge cases here
    # TODO: If the user-place combination already exist, do not create a new one.
    if request.user.is_authenticated and request.method == 'GET':
        place = Places.objects.get(id=request.GET["place"])
        visit = Visit(user=request.user, place=place)
        visit.save()
        return HttpResponse(request.__str__())
    return HttpResponse("User not authenticated or request error")


def remove_visit(request):
    if request.user.is_authenticated and request.method == 'GET':
        Visit.objects.filter(user=request.user, place=request.GET["place"]).delete()
        return HttpResponse("visit removed")
    return HttpResponse("User not authenticated or request error")


def mapbox_token(request):
    return HttpResponse(settings.MAPBOX_TOKEN)


def index(request):
    return render(request, 'index.html')
