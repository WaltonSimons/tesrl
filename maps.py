from object import Object
import tcod
from random import random


class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.tile_map = self.create_empty_map(height, width)
        self.fog_noise_map = self.create_fog_noise_map(height, width)
        self.objects = list()

        self.fov_map = self.create_fov_map()

    def create_empty_map(self, height, width):
        res = [[Tile(None, False) for _ in range(height)] for _ in range(width)]
        return res

    def get_tile(self, x, y):
        return self.tile_map[x][y]

    def create_room(self, x1, y1, x2, y2, terrain):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.tile_map[x][y] = Tile(terrain, False)

    def reload_fov_map(self):
        self.fov_map = self.create_fov_map()

    def create_fov_map(self):
        fov_map = tcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                tcod.map_set_properties(fov_map, x, y, not self.tile_map[x][y].block_sight,
                                        not self.tile_map[x][y].block)
        return fov_map

    def create_fog_noise_map(self, height, width):
        res = [[(random() * 0.02) for _ in range(height)] for _ in range(width)]
        return res


class Tile:
    def __init__(self, terrain, visited):
        self.terrain = terrain
        self.visited = visited

    def __getattr__(self, item):
        if hasattr(self.terrain, item):
            return getattr(self.terrain, item)


class Room:
    def __init__(self, tile_map, exits):
        self.tile_map = tile_map
        self.exits = exits

    @property
    def size(self):
        return len(self.tile_map), len(self.tile_map[0])

    @staticmethod
    def rotated(rotations, room):
        if rotations == 0:
            return room
        else:
            tile_map = list(zip(*room.tile_map))[::-1]
            exits = Room.rotate_exits(room.exits, room.size)

            room = Room(tile_map, exits)
            return Room.rotated(rotations-1, room)

    @staticmethod
    def rotate_exits(exits, size):
        res = list()
        for exit_point in exits:
            res.append((size[1] - exit_point[1] - 1, exit_point[0]))
        return res
