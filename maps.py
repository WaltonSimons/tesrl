from object import Terrain
from loader import load_tiles
import tcod
from random import random


class Map:
    def __init__(self, height, width):
        self.tiles = load_tiles()
        self.height = height
        self.width = width
        self.tile_map = self.create_empty_map(height, width)
        self.fog_noise_map = self.create_fog_noise_map(height, width)
        self.create_room(20, 10, 60, 25, self.tiles['Floor'])
        self.create_room(17, 20, 19, 20, self.tiles['Floor'])
        self.create_room(42, 20, 70, 35, self.tiles['Water'])
        self.create_room(30, 15, 31, 15, self.tiles['Wall'])

        self.fov_map = self.create_fov_map()

    def create_empty_map(self, height, width):
        wall = self.tiles['Wall']
        res = [[Tile(wall, False) for _ in range(height)] for _ in range(width)]
        return res

    def get_tile(self, x, y):
        return self.tile_map[x][y]

    def create_room(self, x1, y1, x2, y2, terrain):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.tile_map[x][y] = Tile(terrain, False)

    def create_fov_map(self):
        fov_map = tcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                tcod.map_set_properties(fov_map, x, y, not self.tile_map[x][y].block_sight, not self.tile_map[x][y].block)
        return fov_map

    def create_fog_noise_map(self, height, width):
        res = [[(random()*0.02) for _ in range(height)] for _ in range(width)]
        return res

class Tile:
    def __init__(self, terrain, visited):
        self.terrain = terrain
        self.visited = visited

    def __getattr__(self, item):
        if hasattr(self.terrain, item):
            return getattr(self.terrain, item)
