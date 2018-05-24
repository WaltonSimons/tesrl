from yaml import load
import tcod
from enum import Enum


class Game:
    def __init__(self):
        self.controls = Controls()
        self.current_map = None
        self.player = None
        self.game_state = GameState.PLAYING
        self.last_player_action = None


class Controls:
    def __init__(self):
        self.actions = self.load_controls()

    def load_controls(self):
        raw = load(open('config/controls.yaml'))
        res = dict()
        for action, keys in raw.items():
            key_codes = list()
            for key_code in keys:
                if hasattr(tcod, key_code):
                    key_codes.append(getattr(tcod, key_code))
                elif len(key_code) == 1:
                    key_codes.append(key_code.lower())
            res[action] = key_codes
        return res


class GameState(Enum):
    PLAYING = 'playing'


class PlayerAction(Enum):
    TAKETURN = 'take_turn'


GAME = Game()
