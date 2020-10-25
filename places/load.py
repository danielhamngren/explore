from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Places
import requests
import json
import os
from string import Template
import osmjson2geojson


# Auto-generated `LayerMapping` dictionary for Places model
places_mapping = {
    'id': 'id',
    'amenity': 'amenity',
    'name': 'name',
    'website': 'website',
    'cuisine': 'cuisine',
    'geom': 'POINT',
}

restaurant_shp = Path(__file__).resolve().parent / 'data' / 'git_d' / 'restaurants_malmo_union.shp'
cafe_shp = Path(__file__).resolve().parent / 'data' / 'git_d' / 'cafes_malmo_union.shp'
fast_food_shp = Path(__file__).resolve().parent / 'data' / 'git_d' / 'fast_food_malmo_union.shp'

OVERPASS_QUERY = """[out:json][timeout:25];
// fetch area “Malmö kommun” to search in
area(3600935416)->.searchArea;
// gather results
(
  // query part for: “amenity=cafe”
  node["amenity"="cafe"](area.searchArea);
  way["amenity"="cafe"](area.searchArea);
  relation["amenity"="cafe"](area.searchArea);
  // query part for: “amenity=restaurant”
  node["amenity"="restaurant"](area.searchArea);
  way["amenity"="restaurant"](area.searchArea);
  relation["amenity"="restaurant"](area.searchArea);
  // query part for: “amenity=fast_food”
  node["amenity"="fast_food"](area.searchArea);
  way["amenity"="fast_food"](area.searchArea);
  relation["amenity"="fast_food"](area.searchArea);
);
// get center points
out center;"""

def run(verbose=True):
    lm = LayerMapping(Places, restaurant_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

    lm = LayerMapping(Places, cafe_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

    lm = LayerMapping(Places, fast_food_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

def web_load(verbose=True):
    # 1. [x] Remove old file if any
    # 2. [x] Make query
    # 3. [x] convert osmjson to geojson
    # 4. [x] Save geojson to file
    # 5. [x] Check if any venue doesn't exist in new set.
    # 6. [x] Mark those as inactive.
    # 7. [x] Update and add new venues.

    overpass_url = "http://overpass-api.de/api/interpreter"

    response = requests.get(overpass_url, params={'data': OVERPASS_QUERY})

    geojson = osmjson2geojson.convert(json.loads(response.text))

    osm_id_list = []
    for feature in geojson['features']:
        osm_id_list.append(['id'])

    # set active the ids in the list
    queryset = Places.objects.filter(id__in=osm_id_list)
    queryset.update(active=True)

    # set inactive the ids not in the list
    queryset = Places.objects.all().exclude(id__in=osm_id_list)
    queryset.update(active=False)

    temp_path = Path(__file__).resolve().parent / 'data' / "temp.json"

    os.remove(temp_path)
    geojson_file = open(temp_path, "w")
    geojson_file.write(json.dumps(geojson))
    geojson_file.close()

    lm = LayerMapping(Places, temp_path.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

