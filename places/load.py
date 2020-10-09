from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from .models import Places


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