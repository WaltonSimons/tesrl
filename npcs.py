import random

class AI:
    def take_turn(self, npc):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        npc.move(x, y)