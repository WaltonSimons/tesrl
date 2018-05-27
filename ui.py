import tcod


class UI:
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.console = tcod.console_new(width, height)

    def blit(self):
        self.draw_everything()
        tcod.console_blit(self.console, 0, 0, self.width, self.height, 0, self.x, self.y)

    def draw_everything(self):
        self.draw_bars()
        self.draw_numbers()
        self.draw_texts()

    def draw_bars(self):
        player_stats = self.game.player.get_component('Creature')
        UIUtils.render_bar(self.console, 1, self.height - 2, 10, player_stats.fatigue, player_stats.max_fatigue,
                           tcod.dark_green, tcod.darkest_green)
        UIUtils.render_bar(self.console, 1, self.height - 4, 10, player_stats.magicka, player_stats.max_magicka,
                           tcod.dark_azure, tcod.darkest_azure)
        UIUtils.render_bar(self.console, 1, self.height - 6, 10, player_stats.health, player_stats.max_health,
                           tcod.dark_red, tcod.darkest_red)

    def draw_numbers(self):
        player_stats = self.game.player.get_component('Creature')
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_print_ex(self.console, 2, self.height - 2, tcod.BKGND_NONE, tcod.LEFT,
                              '{}/{}'.format(player_stats.fatigue, player_stats.max_fatigue))
        tcod.console_print_ex(self.console, 2, self.height - 4, tcod.BKGND_NONE, tcod.LEFT,
                              '{}/{}'.format(player_stats.magicka, player_stats.max_magicka))
        tcod.console_print_ex(self.console, 2, self.height - 6, tcod.BKGND_NONE, tcod.LEFT,
                              '{}/{}'.format(player_stats.health, player_stats.max_health))

    def draw_texts(self):
        player_stats = self.game.player.get_component('Creature')
        player_weapons = player_stats.equipment.get_weapons()
        tcod.console_set_default_foreground(self.console, tcod.white)
        y = self.height - 6
        for weapon in player_weapons:
            tcod.console_print_ex(self.console, 12, y, tcod.BKGND_NONE, tcod.LEFT, weapon.name)
            y += 2


class UIUtils:
    @staticmethod
    def render_bar(console, x, y, bar_width, value, max_value, color, bg_color):
        width = int(float(value) / max_value * bar_width)
        tcod.console_set_default_background(console, bg_color)
        tcod.console_rect(console, x, y, bar_width, 1, False, tcod.BKGND_SET)

        tcod.console_set_default_background(console, color)
        if value > 0:
            tcod.console_rect(console, x, y, width, 1, False, tcod.BKGND_SET)
