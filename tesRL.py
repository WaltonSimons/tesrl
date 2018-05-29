import tcod
from object import *
from maps import *
from game import GAME, GameState, PlayerAction
from assets import ASSETS
from map_manager import MapManager, MapGen
from ui import UI, MESSAGE_LOG

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'TESRL', False)

game = GAME
ui = UI(GAME, 0, 50, 80, 10)
ui.message_log = MESSAGE_LOG
MESSAGE_LOG.add_message('Welcome to tesRL!')

# level_map = ASSETS.get_map('main', 'test', 'test')
level_map = MapGen.create_random_map(50, 80, sorted(ASSETS.assets.get('rooms').keys()))

player = ASSETS.instantiate('creatures', 'base_player')
game.player = MapManager.place_object_randomly(level_map, player)
game.current_map = level_map

for _ in range(5):
    MapManager.place_creature(level_map, 'draugr', *MapManager.find_random_free_space(game.current_map))


def handle_keys():
    key = tcod.console_wait_for_keypress(True)
    key = key.vk if key.vk is not tcod.KEY_CHAR else chr(key.c)
    player = game.player
    GAME.last_player_action = PlayerAction.OTHER_ACTION
    if key == tcod.KEY_ESCAPE:
        pass
    if key in game.controls.actions['up']:
        if GAME.game_state == GameState.PLAYING:
            x = 0
            y = -1
            player.move_or_attack(x, y)

    elif key in game.controls.actions['down']:
        if GAME.game_state == GameState.PLAYING:
            x = 0
            y = 1
            player.move_or_attack(x, y)

    elif key in game.controls.actions['left']:
        if GAME.game_state == GameState.PLAYING:
            x = -1
            y = 0
            player.move_or_attack(x, y)

    elif key in game.controls.actions['right']:
        if GAME.game_state == GameState.PLAYING:
            x = 1
            y = 0
            player.move_or_attack(x, y)
    elif key in game.controls.actions['up_left']:
        if GAME.game_state == GameState.PLAYING:
            x = -1
            y = -1
            player.move_or_attack(x, y)
    elif key in game.controls.actions['up_right']:
        if GAME.game_state == GameState.PLAYING:
            x = 1
            y = -1
            player.move_or_attack(x, y)
    elif key in game.controls.actions['down_left']:
        if GAME.game_state == GameState.PLAYING:
            x = -1
            y = 1
            player.move_or_attack(x, y)
    elif key in game.controls.actions['down_right']:
        if GAME.game_state == GameState.PLAYING:
            x = 1
            y = 1
            player.move_or_attack(x, y)
    elif key in game.controls.actions['wait']:
        if GAME.game_state == GameState.PLAYING:
            GAME.last_player_action = PlayerAction.TAKE_TURN


def render_level():
    level_map = game.current_map
    player = game.player
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
                    color = (max(min(int(300 * level_map.fog_noise_map[x][y]), 255), 0),) * 3
            tcod.console_set_char_background(0, x, y, color, tcod.BKGND_SET)

    objects = level_map.objects
    for o in sorted(objects,
                    key=lambda x: 0 if not x.get_component('Creature') else x.get_component('Creature').health):
        o.draw()

    tcod.console_blit(0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


while not tcod.console_is_window_closed():
    render_level()
    ui.blit()
    tcod.console_flush()
    for o in game.current_map.objects:
        o.clear()
    handle_keys()
    if game.last_player_action == PlayerAction.TAKE_TURN:
        for o in game.current_map.objects:
            creature = o.get_component('Creature')
            if creature:
                if 'AI' in o.components and not creature.dead:
                    o.get_component('AI').take_turn()
