from .cache import CACHE

import requests
from xml.etree import ElementTree


def get_character_ids(character_names):
    character_id_map = {}
    not_cached = character_names[:]
    for character_name in character_names:
        character_id = get_cached(character_name)
        if character_id is not None:
            not_cached.remove(character_name)
            character_id_map[character_id] = character_name

    if len(not_cached) > 0:
        not_cached_map = get_character_ids_xml(not_cached)
        character_id_map.update(not_cached_map)

    return character_id_map


def get_character_ids_xml(character_names):
    character_id_map = {}
    character_name_csv = ",".join(character_names)
    url = "https://api.eveonline.com/eve/CharacterID.xml.aspx?names=" + character_name_csv
    search_results = requests.get(url)
    root = ElementTree.fromstring(search_results.content)
    rowset = root.find('.//rowset[@name="characters"]')
    for row in rowset.findall("row"):
        character_name = row.get('name')
        character_id = int(row.get('characterID'))
        character_id_map[character_id] = character_name
        cache_character(character_name, character_id)
    return character_id_map


def get_cached(character_name):
    id = CACHE.get(normalize_character_name(character_name))
    return id


def cache_character(character_name, character_id):
    CACHE.set(normalize_character_name(character_name), character_id)


def normalize_character_name(name):
    return name.replace(' ', '_').lower()
