import random
from components import Component


class AI(Component):
    def __init__(self):
        super().__init__()

    def take_turn(self, npc):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        npc.move(x, y)
