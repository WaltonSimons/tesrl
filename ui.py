import tcod


class UI:
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.console = tcod.console_new(width, height)
        self.message_log = None

    def blit(self):
        self.draw_everything()
        tcod.console_blit(self.console, 0, 0, self.width, self.height, 0, self.x, self.y)

    def draw_everything(self):
        self.draw_bars()
        self.draw_numbers()
        self.draw_texts()
        self.draw_messages()

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

    def draw_messages(self):
        x = 25
        width = self.width - x - 1
        tcod.console_rect(self.console, x, 1, width, self.height, True, flag=tcod.BKGND_DEFAULT)
        y = 1
        fade_counter = 0
        for message in self.message_log.messages:
            height = tcod.console_get_height_rect(self.console, x, y, width, self.height, message.text)
            color = message.color * (1 - (fade_counter * 0.1))
            tcod.console_set_default_foreground(self.console, color)
            tcod.console_print_rect_ex(self.console, 25, y, width, self.height, tcod.BKGND_NONE, tcod.LEFT,
                                       message.text)
            y += height
            fade_counter += 1


class UIUtils:
    @staticmethod
    def render_bar(console, x, y, bar_width, value, max_value, color, bg_color):
        width = int(float(value) / max_value * bar_width)
        tcod.console_set_default_background(console, bg_color)
        tcod.console_rect(console, x, y, bar_width, 1, True, tcod.BKGND_SET)

        tcod.console_set_default_background(console, color)
        if value > 0:
            tcod.console_rect(console, x, y, width, 1, True, tcod.BKGND_SET)


class MessageLog:
    def __init__(self, log_limit):
        self.messages = list()
        self.log_limit = log_limit

    def add_message(self, message, color=tcod.white, bg_color=tcod.BKGND_NONE):
        message = Message(message, color, bg_color)
        self.messages.insert(0, message)
        if len(self.messages) > self.log_limit:
            self.messages.pop()


class Message:
    def __init__(self, text, color, bg_color):
        self.text = text
        self.color = color
        self.bg_color = bg_color


MESSAGE_LOG = MessageLog(300)
