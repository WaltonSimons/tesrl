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
        for object in self.parent.get_hostiles():
            if self.object.distance_to(object) < self.object.get_component('Creature').fov:
                self.parent.current_mode = self.parent.fighter


class MeleeFighter(AIMode):
    def __init__(self):
        super().__init__()
        target = None

    def take_turn(self):
        target = GAME.player
        if target:
            if int(self.object.distance_to(target)) > 1:
                x, y = AIUtils.move_to_coordinates_step(self.object.x, self.object.y, target.x, target.y,
                                                        self.object.level_map)
                if x and y:
                    self.object.move(x - self.object.x, y - self.object.y)
            else:
                self.object.get_component('Creature').attack_position(target.x, target.y, self.object.level_map)


class AIUtils:
    @staticmethod
    def move_to_coordinates_step(x, y, dest_x, dest_y, map):
        fov_map = map.fov_map
        path = tcod.path_new_using_map(fov_map, 1)
        tcod.path_compute(path, x, y, dest_x, dest_y)
        x, y = tcod.path_walk(path, True)
        tcod.path_delete(path)
        return x, y
