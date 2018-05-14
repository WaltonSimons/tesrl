from loader import Loader
from yaml import load
from maps import Map
import copy
import random
import components


class Assets:
    def __init__(self):
        self.loader = Loader()

        self.assets = self.load_assets()

    def instantiate(self, category, id):
        return copy.deepcopy(self.get_asset(category, id))

    def get_asset(self, category, id):
        return self.assets.get(category).get(id)

    def load_assets(self):
        return self.loader.load_module('main')

    def get_map(self, module, folder, name):
        raw_meta = load(open('modules/{}/maps/{}/{}.yaml'.format(module, folder, name)))
        raw_map = open('modules/{}/maps/{}/{}.map'.format(module, folder, name))
        legend = raw_meta.get('map_info').get('legend')
        legend = {str(key): self.get_asset('tiles', tile_id) for key, tile_id in legend.items()}
        map_data = raw_map.readlines()
        map_object = Map(len(map_data), len(map_data[0].strip()))
        x = 0
        for line in map_data:
            y = 0
            for tile_id in line.strip():
                map_object.tile_map[y][x].terrain = legend[tile_id]
                y += 1
            x += 1
        map_object.reload_fov_map()
        return map_object


ASSETS = Assets()


class CreatureTemplate:
    def __init__(self):
        self.name = None
        self.character = None
        self.base_attributes = None
        self.modifiers = None
        self.equipment = None
        self.inventory = None
        self.loot = None

    def instantiate(self):
        attributes = copy.deepcopy(random.choice(self.base_attributes))
        creature = components.Creature(
            self.name,
            self.character,
            attributes
        )
        creature.modifiers = self.instantiate_group(random.choice(self.modifiers))
        creature.equipment = self.instantiate_group(random.choice(self.equipment))
        creature.inventory = self.instantiate_group(random.choice(self.inventory))
        creature.loot = self.instantiate_group(random.choice(self.loot))

    def instantiate_group(self, ids_group, category):
        return [ASSETS.instantiate(category, ob_id) for ob_id in ids_group]
