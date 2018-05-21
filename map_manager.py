from assets import ASSETS
from object import Object
from maps import Map
import random
import tcod


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
        exits = list()
        for x in range(50):
            room = random.choice(rooms)
            tries = 3
            while tries > 0:
                room_coordinates = (random.randint(0, width - room.size[0]), random.randint(0, height - room.size[1]))
                free_space = MapGen.check_free_space(taken_spaces_map, room_coordinates, room)
                if free_space:
                    MapGen.reserve_space_for_room(taken_spaces_map, room_coordinates, room)
                    room_positions.append((room_coordinates, room))
                    exits += MapGen.get_exits(room_coordinates, room)
                    tries = 0
                tries -= 1
        MapGen.connect_rooms(taken_spaces_map, exits)
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
                if space_type == 3:
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

    @classmethod
    def get_exits(cls, room_coordinates, room):
        res = list()
        for side, exit_range in room.exits.items():
            for x in range(exit_range[0], exit_range[1]+1):
                if side == 'N':
                    res.append((room_coordinates[0] + x, room_coordinates[1]))
                elif side == 'E':
                    res.append((room_coordinates[0] + room.size[0] - 1, room_coordinates[1] + x))
                elif side == 'S':
                    res.append((room_coordinates[0] + x, room_coordinates[1] + room.size[1] - 1))
                elif side == 'W':
                    res.append((room_coordinates[0], room_coordinates[1] + x))
        return res

    @classmethod
    def connect_rooms(cls, taken_spaces_map, exits):
        path_map = tcod.map_new(len(taken_spaces_map), len(taken_spaces_map[0]))
        for x in range(path_map.width):
            for y in range(path_map.height):
                if (x, y) not in exits:
                    tcod.map_set_properties(path_map, x, y, False, taken_spaces_map[x][y] != 1)
                else:
                    tcod.map_set_properties(path_map, x, y, False, True)
        connected_exits = list()
        for exit in exits:
            if exit not in connected_exits:
                path = tcod.dijkstra_new(path_map, 0)
                destination = None
                while destination in [exit, None] + connected_exits:
                    destination = random.choice(exits)
                tcod.dijkstra_compute(path, exit[0], exit[1])
                if tcod.dijkstra_path_set(path, destination[0], destination[1]):
                    keep_destination = False
                    for index in range(tcod.dijkstra_size(path)):
                        point = tcod.dijkstra_get(path, index)
                        if taken_spaces_map[point[0]][point[1]] == 3:
                            keep_destination = True
                            break
                        taken_spaces_map[point[0]][point[1]] = 3
                    connected_exits.append(exit)
                    if not keep_destination:
                        connected_exits.append(destination)
