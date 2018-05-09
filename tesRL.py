import tcod
from object import *
from maps import *

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'TESRL', False)

objects = list()
level_map = Map(50, 80)

player = Object('@')
player.x = 40
player.y = 25
player.level_map = level_map
objects.append(player)


def handle_keys():
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(0, -1)

    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(0, 1)

    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(-1, 0)

    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
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
    key = tcod.console_wait_for_keypress(True)
    handle_keys()
    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_ESCAPE:
        break
