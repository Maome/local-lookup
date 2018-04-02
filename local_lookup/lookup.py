import logging
from collections import defaultdict
import warnings

import zkill
import esi

SCARY_ITEMS = [21096, 28646]
CYNO_ITEMS = [21096, 28646]
CARRIERS = [23919, 23917, 23915, 23913, 23911, 24483, 22852, 23757]
BLOPS = [22436, 22430, 22428, 22440]

warnings.simplefilter('ignore')
log = logging.getLogger('local_lookup')

class Character(object):
    def __init__(self, name):
        self.name = name
        self.id = esi.get_character_id(name)
        self._update_stats()

    def _update_stats(self):
        """ Fetch killmails, and recompute stats """
        self.cynos = 0
        self.carriers = 0
        self.ratting = 0
        self.expensive_ratting = 0
        self.blops_killed = 0

        killmails = zkill.get_killmails(self.id)
        self.kills = [Killmail(kill) for kill in killmails['kills']]
        self.losses = [Killmail(loss) for loss in killmails['losses']]

        for kill in self.kills:
            for attacker in kill.zkillmail['attackers']:
                if attacker.get('character_id') == self.id:
                    if attacker.get('ship_type_id') in CARRIERS:
                        self.carriers += 1
            if kill.victim.get('ship_type_id') in BLOPS:
                self.blops_killed += 1

        for loss in self.losses:
            if loss.is_ratting:
                self.ratting += 1
                if loss.zkillmail['zkb']['totalValue'] > 1000000000:
                    self.expensive_ratting += 1

            if loss.is_cyno:
                self.cynos += 1

            if loss.victim.get('ship_id_type') in CARRIERS:
                self.carriers += 1

    def to_dict(self):
        """ Create a dict out of the Character for serialization (jsonify) """
        value = dict(
            name=self.name,
            id=self.id,
            cynos=self.cynos,
            carriers=self.carriers,
            ratting=self.ratting,
            expensive_ratting=self.expensive_ratting,
            blops_killed=self.blops_killed
        )
        return value

class Killmail(object):
    def __init__(self, zkillmail):
        self.zkillmail = zkillmail
        self.victim = self.zkillmail['victim']
        self.victim_id = self.victim.get('character_id')
        self.items = [entry['item_type_id'] for entry in self.victim['items']]
        self.character_name = None
        self.is_scary = False
        self.is_cyno = False
        self.is_ratting = False

        if self.victim_id:
            self.character_name = esi.get_character(self.victim_id)['name']

        for item in self.items:
            if item in SCARY_ITEMS:
                self.is_scary = True
            if item in CYNO_ITEMS:
                self.is_cyno = True

        for attacker in self.zkillmail['attackers']:
            if attacker.get('character_id') is None:
                self.is_ratting = True
