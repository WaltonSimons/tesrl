from assets import ASSETS
from object import Object
from maps import Map
import random


class MapManager:
    @staticmethod
    def place_object(map, item, x, y):
        class_name = type(item).__name__
        map_object = Object(item.character)
        map_object.set_position(x, y)
        map_object.components[class_name] = item
        map.objects.append(map_object)
        return map_object

    @staticmethod
    def place_creature(map, creature_id, x, y):
        creature = ASSETS.instantiate('creatures', creature_id)
        return MapManager.place_object(map, creature, x, y)


class MapGen:
    @staticmethod
    def create_random_map(height, width, room_ids):
        rooms = [ASSETS.get_asset('rooms', room_id) for room_id in room_ids]
        # 0 - free
        # 1 - occupied by room
        # 2 - corridor only
        # 3 - corridor
        taken_spaces_map = [[0 for _ in range(height)] for _ in range(width)]
        room_positions = list()
        for x in range(10):
            room = random.choice(rooms)
            tries = 3
            while tries > 0:
                room_coordinates = (random.randint(0, width - room.size[1]), random.randint(0, height - room.size[0]))
                free_space = MapGen.check_free_space(taken_spaces_map, room_coordinates, room)
                if free_space:
                    MapGen.reserve_space_for_room(taken_spaces_map, room_coordinates, room)
                    room_positions.append((room_coordinates, room))
                    tries = 0
                tries -= 1
        return MapGen.generate_map(taken_spaces_map, room_positions, height, width)

    @classmethod
    def reserve_space_for_room(cls, taken_spaces_map, room_coordinates, room):
        size = room.size
        corridor_only = ((room_coordinates[0] - 2, room_coordinates[0] + size[0] + 2),
                         (room_coordinates[1] - 2, room_coordinates[1] + size[1] + 2))
        for x in range(len(taken_spaces_map)):
            for y in range(len(taken_spaces_map[0])):
                if room_coordinates[0] <= x < room_coordinates[0] + size[0] \
                and room_coordinates[1] <= y < room_coordinates[1] + size[1]:
                    taken_spaces_map[x][y] = 1
                elif corridor_only[0][0] <= x < corridor_only[0][1] \
                and corridor_only[1][0] <= y < corridor_only[1][1]:
                    taken_spaces_map[x][y] = 2

    @classmethod
    def check_free_space(cls, taken_spaces_map, room_coordinates, room):
        for x in range(room_coordinates[0], room_coordinates[0] + room.size[0]):
            for y in range(room_coordinates[1], room_coordinates[1] + room.size[1]):
                if taken_spaces_map[x][y] != 0:
                    return False
        return True

    @classmethod
    def generate_map(cls, taken_spaces_map, room_positions, height, width):
        res = Map(height, width)
        for x, line in enumerate(taken_spaces_map):
            for y, space_type in enumerate(line):
                if space_type == 2:
                    res.tile_map[x][y].terrain = ASSETS.get_asset('tiles', 'base_floor')
                else:
                    res.tile_map[x][y].terrain = ASSETS.get_asset('tiles', 'base_wall')
        for coordinates, room in room_positions:
            MapGen.place_room(res, room, coordinates)
        res.reload_fov_map()
        return res

    @classmethod
    def place_room(cls, _map, room, coordinates):
        for x in range(coordinates[0], coordinates[0] + room.size[0]):
            for y in range(coordinates[1], coordinates[1] + room.size[1]):
                tile_id = room.tile_map[x - coordinates[0]][y - coordinates[1]]
                _map.tile_map[x][y].terrain = ASSETS.get_asset('tiles', tile_id)
