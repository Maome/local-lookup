import logging
import requests

from bravado.client import SwaggerClient

from cache import cache

ESI_URL = "http://esi.tech.ccp.is/latest/swagger.json"
SWAGGER = SwaggerClient.from_url(ESI_URL)

log = logging.getLogger('local_lookup')

@cache
def get_character_id(name):
    """ Get character by name, this is very slow """
    log.debug('ESI getting character id: %s', name)
    result = SWAGGER.Search.get_search(
        search=name,
        categories=['character'],
        strict=True).result()
    character_ids = result['character']
    if not character_ids:
        raise Exception("Character not found")
    return character_ids[0]

@cache
def get_character(id):
    """ Get character information by character id, this is slow """
    log.debug('ESI getting character for id: %s', str(id))
    result = SWAGGER.Character.get_characters_character_id(character_id=id).result()
    return result

@cache
def get_type_name(type_id):
    """ Get type name by id, works for ships and items, this is slow """
    log.debug('ESI getting type name for id: %s', str(type_id))
    result = SWAGGER.Universe.get_universe_types_type_id(type_id=str(type_id)).result()
    return result['name']
