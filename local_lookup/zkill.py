import logging
import requests

import esi

ZKILL_URL = "https://zkillboard.com/api"
HEADERS = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}

log = logging.getLogger('local_lookup')

def get_killmails(character_id):
    """
    Gets killmails (kills and losses) for a given character_id.
    Returns a dict with keys 'kills' and 'losses'.
    """
    url = "{base}/characterID/{id}/".format(base=ZKILL_URL, id=character_id)
    results = requests.get(url, headers=HEADERS).json()
    killmails = dict(kills=[], losses=[])
    for killmail in results:
        if killmail['victim'].get('character_id') == character_id:
            killmails['losses'].append(killmail)
        else:
            killmails['kills'].append(killmail)

    return killmails
