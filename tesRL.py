import tcod
from object import *
from maps import *
from game import GAME
from assets import Assets
from random import random
from equipment import EquipmentSlots

ASSETS = Assets()

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'TESRL', False)

game = GAME

objects = list()
level_map = ASSETS.get_map('main', 'test', 'test')

player = Object('@')
player.x = 40
player.y = 25
player.components['Creature'] = ASSETS.instantiate('creatures', 'base_player')
game.current_map = level_map
objects.append(player)
dagger = ASSETS.instantiate('items', 'iron_dagger')
player.get_component('Creature').equip(dagger, EquipmentSlots.RIGHT_HAND)
player.get_component('Creature').unequip(dagger)

player2 = Object('@')
player2.x = 45
player2.y = 20
objects.append(player2)


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
    level_map = game.current_map
    tcod.map_compute_fov(game.current_map.fov_map, player.x, player.y, player.get_component('Creature').fov, True, 0)
    for y in range(level_map.height):
        for x in range(level_map.width):
            visible = tcod.map_is_in_fov(game.current_map.fov_map, x, y)
            tile = level_map.get_tile(x, y)
            color = tile.color
            if visible:
                tile.visited = True
            else:
                if tile.visited:
                    color = list(map(lambda a: max(min(int(a * (0.3 + level_map.fog_noise_map[x][y])), 255), 0), color))
                else:
                    color = (max(min(int(500 * level_map.fog_noise_map[x][y]), 255), 0),) * 3
            tcod.console_set_char_background(0, x, y, color, tcod.BKGND_SET)

    for o in objects:
        o.draw()

    tcod.console_blit(0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


while not tcod.console_is_window_closed():
    render_level()
    tcod.console_flush()
    for o in objects:
        o.clear()
    handle_keys()
