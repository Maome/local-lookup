from . import esi

"""
Items:
cyno:        21096
covert cyno: 28646

"""


def is_scary_item(item_type_id):
    if item_type_id == 21096:
        return True
    elif item_type_id == 28646:
        return True
    return False


def get_scary_item_name(item_type_id):
    if item_type_id == 21096:
        return "cyno"
    elif item_type_id == 28646:
        return "covert cyno"
    return ""


def process_character_losses(character_id_map, character_losses):
    processed_data = []
    for killmail in character_losses:
        victim = killmail["victim"]
        for item in victim["items"]:
            item_type_id = item["item_type_id"]
            if is_scary_item(item_type_id):
                processed_data.append(process_loss_info(character_id_map, killmail, item_type_id))
                break
    return processed_data


def process_loss_info(character_id_map, killmail, item_type_id):
    processed_loss = {}
    victim = killmail["victim"]

    processed_loss['character_name'] = character_id_map[victim["character_id"]]
    processed_loss['killmail_time'] = killmail["killmail_time"]
    processed_loss['ship_name'] = esi.get_ship_name(str(victim["ship_type_id"]))
    processed_loss['item_discovered'] = get_scary_item_name(item_type_id)

    return processed_loss
