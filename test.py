import random
import string

import tcod

size = 50

tcod.console_init_root(size, size, 'Test', False)


while(True):
    key = tcod.console_wait_for_keypress(True)
    if key.vk == tcod.KEY_SPACE:
        for x in range(size):
            for y in range(size):
                tcod.console_set_default_foreground(0, (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                tcod.console_put_char(0, x, y, random.choice(string.ascii_letters), tcod.BKGND_NONE)

        tcod.console_flush()
    