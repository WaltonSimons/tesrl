from functools import wraps
from game import GAME, PlayerAction


def player_action(func):
    def _decorator(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if request is GAME.player or request is GAME.player.get_component('creature'):
            GAME.last_player_action = PlayerAction.TAKE_TURN
        return response

    return wraps(func)(_decorator)
