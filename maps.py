from object import Terrain
from loader import load_tiles
import tcod


class Map:
    def __init__(self, height, width):
        self.tiles = load_tiles()
        self.height = height
        self.width = width
        self.tile_map = self.create_empty_map(height, width)
        self.create_room(20, 10, 60, 25, self.tiles['Floor'])
        self.create_room(40, 20, 70, 35, self.tiles['Water'])

    def create_empty_map(self, height, width):
        res = [[self.tiles['Wall'] for y in range(height)] for x in range(width)]
        return res

    def get_tile(self, x, y):
        return self.tile_map[x][y]

    def create_room(self, x1, y1, x2, y2, tile):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.tile_map[x][y] = tile
