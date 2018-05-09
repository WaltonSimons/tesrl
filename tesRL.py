import tcod
from object import *
from maps import *
from game import Game

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'TESRL', False)

game = Game()

objects = list()
level_map = Map(50, 80)

player = Object('@')
player.x = 40
player.y = 25
player.level_map = level_map
objects.append(player)


def handle_keys():
    key = tcod.console_wait_for_keypress(True)
    key = key.vk if key.vk is not tcod.KEY_CHAR else chr(key.c)
    if key == tcod.KEY_ESCAPE:
        pass
    if key in game.controls.actions['up']:
        player.move(0, -1)

    elif key in game.controls.actions['down']:
        player.move(0, 1)

    elif key in game.controls.actions['left']:
        player.move(-1, 0)

    elif key in game.controls.actions['right']:
        player.move(1, 0)


def render_level():
    for y in range(level_map.height):
        for x in range(level_map.width):
            terrain = level_map.get_tile(x, y)
            tcod.console_set_char_background(0, x, y, terrain.color, tcod.BKGND_SET)

    for o in objects:
        o.draw()

    tcod.console_blit(0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


while not tcod.console_is_window_closed():
    render_level()
    tcod.console_flush()
    for o in objects:
        o.clear()
    handle_keys()