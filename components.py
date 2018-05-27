import math
from equipment import CreatureEquipment
from enum import Enum
import tcod


class Component:
    def __init__(self):
        self.comp_name = type(self).__name__
        self.parent = None


class Creature(Component):
    def __init__(self, name, character, base_attributes, color=tcod.white):
        super().__init__()
        self.name = name
        self.character = character
        self.color = color
        self.base_attributes = base_attributes
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
        self.dead = False

    def equip(self, item, slot):
        if item not in self.inventory:
            self.add_to_inventory(item)
        self.equipment.equip(item, slot)

    def unequip(self, item):
        self.equipment.unequip(item)

    def add_to_inventory(self, item):
        if item.stackable:
            found = False
            for inv_item in self.inventory:
                if inv_item.object_id == item.object_id:
                    inv_item.quantity += item.quantity
                    found = True
                    break
            if not found:
                self.inventory.append(item)
        else:
            self.inventory.append(item)

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
        return int((self.strength + self.endurance) / 2)

    def get_max_magicka(self):
        return int((self.intelligence + self.willpower) / 2)

    def get_fatigue(self):
        return int(self.willpower + self.strength + self.agility + self.endurance)

    def get_encumbrance(self):
        return 5 * self.strength

    @property
    def fov(self):
        return int(4 + (math.sqrt(self.agility) * (3 / 2)))

    def attack_position(self, x, y, level_map):
        target = level_map.get_object_on_position(x, y)
        if target:
            creature = target.get_component('Creature')
            if creature:
                weapons = self.equipment.get_weapons()
                damage = 0  # TODO: Damage class
                for weapon in weapons:
                    damage += weapon.base_damage
                creature.take_damage(damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.dead = True
        self.parent.char = 'c'


class Modifier:
    def __init__(self, name, object_id, modifier_type):
        self.name = name
        self.modifier_type = modifier_type
        self.object_id = object_id
        self.attributes = None


class ModifierTypes(Enum):
    RACE = 'race'
    LIFEFORM = 'lifeform'


class Attributes:
    def __init__(self, agility, endurance, intelligence, luck, personality, strength, willpower):
        self.agility = agility
        self.endurance = endurance
        self.intelligence = intelligence
        self.luck = luck
        self.personality = personality
        self.strength = strength
        self.willpower = willpower


class CreatureTemplate:
    def __init__(self, object_id):
        self.name = None
        self.object_id = object_id
        self.character = None
        self.color = None
        self.base_attributes = None
        self.modifiers = None
        self.equipment = None
        self.inventory = None
        self.loot = None
