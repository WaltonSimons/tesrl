from object import TileType, Object
import components
import tcod
import os
import copy

from yaml import load


class Loader:
    def load_module(self, name):
        print('Loading module {}'.format(name))
        path = 'modules/{}/'.format(name)
        self.assets_dict = dict()
        print('Loading tile types')
        tiles = self.load_tiles(path)
        self.assets_dict['tiles'] = tiles
        print('Loading races')
        races = self.load_races(path)
        self.assets_dict['races'] = races
        print('Loading creatures')
        creatures = self.load_creatures(path)
        self.assets_dict['creatures'] = creatures

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

    def load_races(self, path):
        path = path + 'races/'
        race_files = os.listdir(path)
        races = dict()
        for race_file_name in race_files:
            print('Loading {}'.format(race_file_name))
            raw = load(open(path + race_file_name))
            for raw_race in raw.get('race_presets'):
                raw_attributes = raw_race.get('attributes')
                attributes = components.Attributes(
                    raw_attributes.get('agility', 0),
                    raw_attributes.get('endurance', 0),
                    raw_attributes.get('intelligence', 0),
                    raw_attributes.get('luck', 0),
                    raw_attributes.get('personality', 0),
                    raw_attributes.get('strength', 0),
                    raw_attributes.get('willpower', 0)
                )
                race = components.Modifier(
                    raw_race.get('name'),
                )
                race.attributes = attributes
                races[race.name] = race
        return races

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
                creature = components.Creature(
                    name,
                    character,
                    raw_attributes.get('agility', 0),
                    raw_attributes.get('endurance', 0),
                    raw_attributes.get('intelligence', 0),
                    raw_attributes.get('luck', 0),
                    raw_attributes.get('personality', 0),
                    raw_attributes.get('strength', 0),
                    raw_attributes.get('willpower', 0)
                )
                if race in self.assets_dict['races']:
                    creature.modifiers.append(copy.deepcopy(self.assets_dict['races'][race]))
                creatures[object_id] = creature
        return creatures
