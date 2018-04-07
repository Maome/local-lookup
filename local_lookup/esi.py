from .cache import cache

import requests


@cache()
def get_ship_name(ship_type_id):
    url = "https://esi.tech.ccp.is/latest/universe/types/" + ship_type_id + "/"
    search_results = requests.get(url)

    return search_results.json()["name"]
