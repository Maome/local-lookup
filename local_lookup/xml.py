import logging

from xml.etree import ElementTree

log = logging.getLogger('local_lookup')

def get_character_ids(character_names):
    """ Get many character IDs from character names, this is slow """
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
    return character_id_map
