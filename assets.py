from loader import Loader
from yaml import load
from maps import Map
import copy
import random
import components
from equipment import EquipmentSlots


class Assets:
    def __init__(self):
        self.loader = Loader()

        self.assets = self.load_assets()

    def instantiate(self, category, id):
        if category != 'creatures':
            res = copy.deepcopy(self.get_asset(category, id))
        else:
            res = self.instantiate_creature(self.get_asset('creatures', id))
        return res

    def get_asset(self, category, id):
        return self.assets.get(category).get(id)

    def load_assets(self):
        return self.loader.load_module('main')

    def get_map(self, module, folder, name):
        return self.loader.load_map(module, folder, name)

    def instantiate_creature(self, creature_template):
        attributes = copy.deepcopy(random.choice(creature_template.base_attributes))
        creature = components.Creature(
            creature_template.name,
            creature_template.character,
            attributes,
            creature_template.color
        )
        creature.modifiers = self.instantiate_group(random.choice(creature_template.modifiers), 'modifiers')
        for slot, item in creature_template.equipment.items():
            creature.equip(ASSETS.instantiate('items', item), EquipmentSlots(slot))
        if creature_template.inventory:
            for object_id, quantity in creature_template.inventory.items():
                item = self.instantiate('items', object_id)
                if quantity:
                    limits = [int(val) for val in quantity.split('...')]
                    item.quantity = random.randint(limits[0], limits[1])
                creature.add_to_inventory(item)
        if creature_template.loot:
            for object_id, quantity in creature_template.loot.items():
                item = self.instantiate('items', object_id)
                if quantity:
                    limits = [int(val) for val in quantity.split('...')]
                    item.quantity = random.randint(limits[0], limits[1])
                creature.loot.append(item)
        return creature

    def instantiate_group(self, ids_group, category):
        return [ASSETS.instantiate(category, ob_id) for ob_id in ids_group]


ASSETS = Assets()
