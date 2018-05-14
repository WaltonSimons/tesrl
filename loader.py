from object import TileType, Object
import components
import equipment
import tcod
import os
import copy

from yaml import load


class Loader:
    def __init__(self):
        self.assets_dict = dict()

    def load_module(self, name):
        print('Loading module {}'.format(name))
        path = 'modules/{}/'.format(name)
        print('Loading tile types')
        tiles = self.load_tiles(path)
        self.assets_dict['tiles'] = tiles
        print('Loading modifiers')
        modifiers = self.load_modifiers(path)
        self.assets_dict['modifiers'] = modifiers
        print('Loading creatures')
        creatures = self.load_creatures(path)
        self.assets_dict['creatures'] = creatures
        print('Loading items')
        items = self.load_items(path)
        self.assets_dict['items'] = items

        return self.assets_dict

    def load_tiles(self, path):
        path = path + 'tiles/'
        tile_files = os.listdir(path)
        tiles = dict()
        for tile_file_name in tile_files:
            print('Loading {}'.format(tile_file_name))
            raw = load(open(path + tile_file_name))
            for raw_tile in raw.get('tiles'):
                name = raw_tile.get('name')
                object_id = raw_tile.get('id')
                color = raw_tile.get('color')
                if hasattr(tcod, color):
                    color = getattr(tcod, color)
                else:
                    continue
                block = raw_tile.get('block')
                block_sight = raw_tile.get('block_sight')
                if object_id in tiles:
                    print('Tile with id {} already exists and will be overwritten.'.format(object_id))
                tiles[object_id] = (TileType(name, object_id, color, block, block_sight))
        return tiles

    def load_modifiers(self, path):
        path = path + 'modifiers/'
        modifier_files = os.listdir(path)
        modifiers = dict()
        for modifier_file_name in modifier_files:
            print('Loading {}'.format(modifier_file_name))
            raw = load(open(path + modifier_file_name))
            for raw_modifier in raw.get('modifiers'):
                raw_attributes = raw_modifier.get('attributes')
                attributes = components.Attributes(
                    raw_attributes.get('agility', 0),
                    raw_attributes.get('endurance', 0),
                    raw_attributes.get('intelligence', 0),
                    raw_attributes.get('luck', 0),
                    raw_attributes.get('personality', 0),
                    raw_attributes.get('strength', 0),
                    raw_attributes.get('willpower', 0)
                )
                modifier_type = raw_modifier.get('type')
                modifier = components.Modifier(
                    raw_modifier.get('name'),
                    raw_modifier.get('id'),
                    components.ModifierTypes(modifier_type)
                )
                modifier.attributes = attributes
                modifiers[modifier.name] = modifier
        return modifiers

    def load_creatures(self, path):
        path = path + 'creatures/'
        creature_files = os.listdir(path)
        creatures = dict()
        for creature_file_name in creature_files:
            print('Loading {}'.format(creature_file_name))
            raw = load(open(path + creature_file_name))
            for raw_creature in raw.get('creature_presets'):
                object_id = raw_creature.get('id')
                name = raw_creature.get('name')
                race = raw_creature.get('race')
                character = raw_creature.get('character')
                raw_attributes = raw_creature.get('attributes')
                attributes = components.Attributes(
                    raw_attributes.get('agility', 0),
                    raw_attributes.get('endurance', 0),
                    raw_attributes.get('intelligence', 0),
                    raw_attributes.get('luck', 0),
                    raw_attributes.get('personality', 0),
                    raw_attributes.get('strength', 0),
                    raw_attributes.get('willpower', 0)
                )
                creature = components.Creature(
                    name,
                    character,
                    attributes,
                )
                if race in self.assets_dict['modifiers']:
                    creature.modifiers.append(copy.deepcopy(self.assets_dict['modifiers'][race]))
                creatures[object_id] = creature
        return creatures

    def load_items(self, path):
        path = path + 'items/'
        item_files = os.listdir(path)
        items = dict()
        for item_file_name in item_files:
            print('Loading {}'.format(item_file_name))
            raw = load(open(path + item_file_name))
            for raw_weapon in raw.get('weapons'):
                object_id = raw_weapon.get('id')
                name = raw_weapon.get('name')
                value = raw_weapon.get('value')
                base_damage = raw_weapon.get('base_damage')
                two_handed = raw_weapon.get('two_handed')
                weapon = equipment.Weapon(
                    name,
                    object_id,
                    base_damage,
                    two_handed
                )
                items[object_id] = weapon
        return items
