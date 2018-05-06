import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'TESRL', False)

while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0, tcod.white)
    tcod.console_put_char(0, 1, 1, '@', tcod.BKGND_NONE)
    tcod.console_flush()

 