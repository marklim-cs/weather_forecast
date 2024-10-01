import json
from django.core.cache import cache

def list_of_cities():
    cities = cache.get()
    if not cities:
        with open('app/static/data/current.city.list.json', 'r') as f:
            cities = json.load(f)

            cache.set('city_list', cities, timeout=None)
    return cities