from assets import ASSETS
from object import Object


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
