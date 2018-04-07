from .cache import cache

import requests


@cache(time=5)
def get_character_losses(character_id_map):
    # take the keys for the dictionary as a list
    character_ids = list(character_id_map)
    # zkillboard requires the ids to be sorted for its api
    character_ids.sort()
    character_id_str = ",".join(str(i) for i in character_ids)
    url = "https://zkillboard.com/api/losses/characterID/" + character_id_str + "/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)

    return search_results.json()
