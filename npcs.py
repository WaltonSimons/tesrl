import random
import tcod
from components import Component
from game import GAME


class AI(Component):
    def __init__(self):
        super().__init__()
        self.target = GAME.player

    def move_to_coordinates_step(self, x, y, dest_x, dest_y, map):
        fov_map = map.fov_map
        path = tcod.path_new_using_map(fov_map, 1)
        tcod.path_compute(path, x, y, dest_x, dest_y)
        x, y = tcod.path_walk(path, True)
        tcod.path_delete(path)
        return x, y

    def take_turn(self):
        target = self.target
        if target:
            if int(self.parent.distance_to(target)) > 1:
                x, y = self.move_to_coordinates_step(self.parent.x, self.parent.y, target.x, target.y, self.parent.level_map)
                if x and y:
                    self.parent.move(x - self.parent.x, y - self.parent.y)
            else:
                self.parent.get_component('Creature').attack_position(target.x, target.y, self.parent.level_map)
