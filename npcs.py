import random
import tcod
from components import Component
from game import GAME


class AI(Component):
    def __init__(self):
        super().__init__()
        self.target = GAME.player
        self.wanderer = None
        self.fighter = None
        self.add_ai_mode('wanderer', Drunkard())
        self.add_ai_mode('fighter', MeleeFighter())
        self.current_mode = self.wanderer

    def add_ai_mode(self, mode_name, mode_class):
        mode_class.parent = self
        setattr(self, mode_name, mode_class)

    def take_turn(self):
        self.current_mode.take_turn()

    def get_hostiles(self):
        return [GAME.player]


class AIMode:
    def __init__(self):
        self.parent = None

    def take_turn(self):
        pass

    @property
    def object(self):
        return self.parent.parent


class Drunkard(AIMode):
    def __init__(self):
        super().__init__()

    def take_turn(self):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        self.object.move(x, y)
        fov = self.object.get_component('Creature').fov
        if AIUtils.get_closest_visible_object_in_range(self, self.parent.get_hostiles(), fov):
            print('Switching to fighter')
            self.parent.current_mode = self.parent.fighter
            self.parent.fighter.set_target()


class MeleeFighter(AIMode):
    def __init__(self):
        super().__init__()
        self.target = None

    def set_target(self):
        fov = self.object.get_component('Creature').fov
        target_object = AIUtils.get_closest_visible_object_in_range(self, self.parent.get_hostiles(), fov)
        if target_object:
            self.target = (target_object.x, target_object.y)
        return target_object

    def take_turn(self):
        target_object = self.set_target()
        if (self.object.x, self.object.y) is not self.target:
            if int(self.object.distance_to_point(self.target[0], self.target[1])) > 1:
                x, y = AIUtils.move_to_coordinates_step(self.object.x, self.object.y, self.target[0], self.target[1],
                                                        self.object.level_map)
                if x and y:
                    self.object.move(x - self.object.x, y - self.object.y)
            else:
                if target_object:
                    self.object.get_component('Creature').attack_position(self.target[0], self.target[1], self.object.level_map)
                else:
                    print('Switching to wanderer')
                    self.parent.current_mode = self.parent.wanderer


class AIUtils:
    @staticmethod
    def move_to_coordinates_step(x, y, dest_x, dest_y, map):
        fov_map = map.fov_map
        path = tcod.path_new_using_map(fov_map, 1)
        tcod.path_compute(path, x, y, dest_x, dest_y)
        x, y = tcod.path_walk(path, True)
        tcod.path_delete(path)
        return x, y

    @staticmethod
    def check_line_of_sight(x, y, x2, y2, map):
        return tcod.line(x, y, x2, y2, lambda xp, yp: not map.get_tile(xp, yp).block_sight)

    @staticmethod
    def get_closest_visible_object_in_range(npc, objects, max_distance):
        closest = None
        distance = max_distance
        for object in objects:
            new_distance = npc.object.distance_to(object)
            if new_distance < distance:
                if AIUtils.check_line_of_sight(npc.object.x, npc.object.y, object.x, object.y, npc.object.level_map):
                    distance = new_distance
                    closest = object
        return closest