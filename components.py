import math
from equipment import CreatureEquipment


class Creature:
    def __init__(self, name, character, agility, endurance, intelligence, luck, personality, strength, willpower):
        self.name = name
        self.character = character
        self.base_attributes = Attributes(agility, endurance, intelligence, luck, personality, strength, willpower)
        self.modifiers = list()
        self.equipment = CreatureEquipment()

        self.max_health = self.get_max_health()
        self.health = self.max_health
        self.max_magicka = self.get_max_magicka()
        self.magicka = self.max_magicka
        self.max_magicka = self.get_max_magicka()
        self.magicka = self.max_magicka
        self.max_fatigue = self.get_fatigue()
        self.fatigue = self.max_fatigue
        self.encumbrance = self.get_encumbrance()
        self.inventory = list()
        self.loot = list()

    def equip(self, item, slot):
        self.equipment.equip(item, slot)

    def unequip(self, item):
        self.equipment.unequip(item)

    def get_attribute(self, name):
        res = getattr(self.base_attributes, name)
        for modifier in self.modifiers:
            if modifier.attributes:
                res += getattr(modifier.attributes, name)
        return res

    @property
    def agility(self):
        return self.get_attribute('agility')

    @property
    def endurance(self):
        return self.get_attribute('endurance')

    @property
    def intelligence(self):
        return self.get_attribute('intelligence')

    @property
    def luck(self):
        return self.get_attribute('luck')

    @property
    def personality(self):
        return self.get_attribute('personality')

    @property
    def strength(self):
        return self.get_attribute('strength')

    @property
    def willpower(self):
        return self.get_attribute('willpower')

    def get_max_health(self):
        return (self.strength + self.endurance) / 2

    def get_max_magicka(self):
        return (self.intelligence + self.willpower) / 2

    def get_fatigue(self):
        return self.willpower + self.strength + self.agility + self.endurance

    def get_encumbrance(self):
        return 5 * self.strength

    @property
    def fov(self):
        return int(4 + (math.sqrt(self.agility) * (3 / 2)))


class Modifier:
    def __init__(self, name, object_id):
        self.name = name
        self.object_id = object_id
        self.attributes = None


class Attributes:
    def __init__(self, agility, endurance, intelligence, luck, personality, strength, willpower, modifier_name=None):
        self.modifier_name = modifier_name
        self.agility = agility
        self.endurance = endurance
        self.intelligence = intelligence
        self.luck = luck
        self.personality = personality
        self.strength = strength
        self.willpower = willpower
