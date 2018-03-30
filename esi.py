#!/usr/bin/env python3
from pprint import pprint

from bravado.client import SwaggerClient
import requests

ESI_URL = "http://esi.tech.ccp.is/latest/swagger.json"
SCARY_ITEMS = [21096, 28646]

CACHED_IDS = {}

def get_client():
    """ Does this need to be instantiated every time? """
    return SwaggerClient.from_url(ESI_URL)

def get_character_id(name):
    print "getting char name"
    result = get_client().Search.get_search(
        search=name,
        categories=['character'],
        strict=True).result()
    character_ids = result['character']
    if not character_ids:
        raise Exception("Character not found")
    return character_ids[0]

def get_character(id):
    print "Getting character"
    result = get_client().Character.get_characters_character_id(character_id=id).result()
    return result

def get_type_name(type_id):
    cached = CACHED_IDS.get(type_id)
    if cached:
        print "Got fast type name"
        return cached
    print "Getting slow type name"
    result = get_client().Universe.get_universe_types_type_id(type_id=type_id).result()
    CACHED_IDS[type_id] = result['name']
    return result['name']


def is_scary_item(item_type_id):
    return item_type_id in SCARY_ITEMS

def process_character_losses(name, character_losses):
    print "processing losses"
    processed_data = []
    for killmail in character_losses:
        victim = killmail["victim"]
        for item in victim["items"]:
            item_type_id = item["item_type_id"]
            if is_scary_item(item_type_id):
                processed_data.append(process_loss_info(name, killmail, item_type_id))
                break
    return processed_data

def process_loss_info(name, killmail, item_type_id):
    print "Processing loss"
    processed_loss = {}
    victim = killmail["victim"]

    processed_loss['character_name'] = name
    processed_loss['killmail_time'] = killmail["killmail_time"]
    processed_loss['ship_name'] = get_type_name(str(victim["ship_type_id"]))
    processed_loss['item_discovered'] = get_type_name(item_type_id)

    return processed_loss

zkill_base_url = "https://zkillboard.com/api"

def get_losses(name):
    print "Getting losses"
    character_id = get_character_id(name)
    url = "{base}/losses/characterID/{id}/".format(base=zkill_base_url, id=character_id)
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)
    return search_results.json()

def go(name):
    import warnings
    warnings.simplefilter('ignore')
    losses = get_losses(name)
    pprint(process_character_losses(name, losses))
