class Creature:
    def __init__(self, name, agility, endurance, intelligence, luck, personality, strength, willpower):
        self.name = name
        self.agility = agility
        self.endurance = endurance
        self.intelligence = intelligence
        self.luck = luck
        self.personality = personality
        self.strength = strength
        self.willpower = willpower
        self.max_health = self.get_max_health()
        self.health = self.max_health
        self.max_magicka = self.get_max_magicka()
        self.magicka = self.max_magicka
        self.max_magicka = self.get_max_magicka()
        self.magicka = self.max_magicka
        self.max_fatigue = self.get_fatigue()
        self.fatigue = self.max_fatigue
        self.encumbrance = self.get_encumbrance()
        self.fov = self.get_fov()
        self.inventory = list()
        self.loot = list()

    def get_max_health(self):
        return (self.strength + self.endurance) / 2

    def get_max_magicka(self):
        return (self.intelligence + self.willpower) / 2

    def get_fatigue(self):
        return self.willpower + self.strength + self.agility + self.endurance

    def get_encumbrance(self):
        return 5 * self.strength

    def get_fov(self):
        return int(self.agility / 3)
