import tcod
from game import GAME


class Object:
    def __init__(self, character, color=tcod.white):
        self.x = None
        self.y = None
        self.char = character[0]
        self.color = color
        self.components = dict()

    def get_component(self, component):
        return self.components[component] if component in self.components else None

    def move(self, dx, dy):
        level_map = GAME.current_map
        if not level_map.tile_map[self.x + dx][self.y + dy].block:
            self.x += dx
            self.y += dy

    def draw(self):
        if tcod.map_is_in_fov(GAME.current_map.fov_map, self.x, self.y):
            tcod.console_set_default_foreground(0, self.color)
            tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(0, self.x, self.y, ' ', tcod.BKGND_NONE)


class TileType:
    def __init__(self, name, object_id, color, block, block_sight):
        self.name = name
        self.object_id = object_id
        self.color = color
        self.block = block
        self.block_sight = block_sight
