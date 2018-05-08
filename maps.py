from object import Terrain
import tcod


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_map = self.create_empty_map(height, width)

    def create_empty_map(self, height, width):
        res = [[Terrain(tcod.azure, False, False) for y in range(height)] for x in range(width)]
        return res

    def get_tile(self, x, y):
        return self.tile_map[x][y]
