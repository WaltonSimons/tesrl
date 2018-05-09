import tcod


class Object:
    def __init__(self, character, color=tcod.white):
        self.x = None
        self.y = None
        self.char = character[0]
        self.color = color
        self.components = dict()
        self.level_map = None

    def get_component(self, component):
        return self.components[component] if component in self.components else None

    def move(self, dx, dy):
        if not self.level_map.tile_map[self.x + dx][self.y + dy].block:
            self.x += dx
            self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(0, self.color)
        tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(0, self.x, self.y, ' ', tcod.BKGND_NONE)


class Terrain:
    def __init__(self, name, color, block, block_sight):
        self.name = name
        self.color = color
        self.block = block
        self.block_sight = block_sight
