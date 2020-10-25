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


def run(verbose=True):
    lm = LayerMapping(Places, restaurant_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

    lm = LayerMapping(Places, cafe_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

    lm = LayerMapping(Places, fast_food_shp.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)

def web_load(verbose=True):
    # 1. [x] Remove old file if any
    # 2. [ ] Make query
    # 3. [x] convert osmjson to geojson
    # 4. [x] Save geojson to file
    # 5. [ ] Check if any venue doesn't exist in new set.
    # 6. [ ] Mark those as inactive.
    # 7. [x] Update and add new venues.


    overpass_url = "http://overpass-api.de/api/interpreter"

    overpass_query = overpass_query_helper('Malmö kommun', 'cafe')
    response = requests.get(overpass_url, params={'data': overpass_query})

    geojson = osmjson2geojson.convert(json.loads(response.text))


    temp_path = Path(__file__).resolve().parent / 'data' / "temp.json"

    os.remove(temp_path)
    geojson_file = open(temp_path, "w")
    geojson_file.write(json.dumps(geojson))
    geojson_file.close()

    lm = LayerMapping(Places, temp_path.as_posix(), places_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


def overpass_query_helper(geocodeArea, amenity):
    # Note that the {{geocodeArea}} is only a helper from overpass turbo
    # it is not actually in the Overpass API
    return Template("""[out:json][timeout:25];
        {{geocodeArea:$geocodeArea}}->.searchArea;
        (
        node["amenity"="$amenity"](area.searchArea);
        way["amenity"="$amenity"](area.searchArea);
        relation["amenity"="$amenity"](area.searchArea);
        );
        out center;""").substitute(geocodeArea=geocodeArea, amenity=amenity)