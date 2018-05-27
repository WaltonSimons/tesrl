import tcod
from game import GAME


class Object:
    def __init__(self, character, color=tcod.white, blocks=False):
        self.x = None
        self.y = None
        self.char = character[0]
        self._color = color
        self._blocks = blocks
        self.components = dict()

    def get_component(self, component):
        return self.components[component] if component in self.components else None

    def add_component(self, component):
        self.components[component.comp_name] = component
        component.parent = self

    def move(self, dx, dy):
        level_map = GAME.current_map
        if not level_map.is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            res = True
        else:
            res = False
        return res

    def draw(self):
        if tcod.map_is_in_fov(GAME.current_map.fov_map, self.x, self.y):
            tcod.console_set_default_foreground(0, self.color)
            tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(0, self.x, self.y, ' ', tcod.BKGND_NONE)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    @property
    def blocks(self):
        creature = self.get_component('Creature')
        if not creature:
            res = self._blocks
        else:
            res = not creature.dead
        return res

    @property
    def color(self):
        for comp_name, component in self.components.items():
            if hasattr(component, 'color'):
                return component.color
        return self._color

class TileType:
    def __init__(self, name, object_id, color, block, block_sight):
        self.name = name
        self.object_id = object_id
        self.color = color
        self.block = block
        self.block_sight = block_sight
