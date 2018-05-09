from object import Terrain, Object
import components
import tcod

from yaml import load


def load_tiles():
    raw = load(open('modules/main/tiles/basic_tiles.yaml'))
    tiles = dict()
    for raw_tile in raw.get('tiles'):
        name = raw_tile.get('name')
        color = raw_tile.get('color')
        if hasattr(tcod, color):
            color = getattr(tcod, color)
        else:
            continue
        block = raw_tile.get('block')
        block_sight = raw_tile.get('block_sight')
        tiles[name] = (Terrain(name, color, block, block_sight))
    load_race_presets()
    return tiles


def load_race_presets():
    raw = load(open('modules/main/creatures/races/playable.yaml'))
    races = dict()
    for raw_race in raw.get('race_presets'):
        race = components.Creature(
            raw_race.get('name'),
            raw_race.get('agility', 0),
            raw_race.get('endurance', 0),
            raw_race.get('intelligence', 0),
            raw_race.get('luck', 0),
            raw_race.get('personality', 0),
            raw_race.get('strength', 0),
            raw_race.get('willpower', 0)
        )
        races[race.name] = race
    return races
