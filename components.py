import math
from equipment import CreatureEquipment
from ui import MESSAGE_LOG
from game import GAME
from enum import Enum
import tcod
import random


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
        target = level_map.get_blocking_object_on_position(x, y)
        if target:
            creature = target.get_component('Creature')
            if creature:
                weapons = self.equipment.get_weapons()
                damage = 0  # TODO: Damage class
                for weapon in weapons:
                    damage += weapon.base_damage

                hit_rate = ((self.agility / 6) + (self.luck / 10)) * (
                0.75 + 0.25 * self.fatigue / self.max_fatigue) * 10
                hit = random.random() < hit_rate / 100
                if hit:
                    dealt_damage, evaded, dead = creature.get_attacked(damage)

                    if not evaded:
                        color = tcod.white
                        if self.parent == GAME.player:
                            message = 'You deal {} damage to {}!'.format(dealt_damage, creature.name)
                        elif creature.parent == GAME.player:
                            message = 'You take {} damage from {}!'.format(dealt_damage, self.name)
                            color = tcod.dark_red
                        else:
                            message = '{} deals {} damage to {}!'.format(self.name, dealt_damage, creature.name)
                        MESSAGE_LOG.add_message(message, color)
                        if dead:
                            MESSAGE_LOG.add_message('{} dies!'.format(creature.name))
                    else:
                        color = tcod.white
                        if self.parent == GAME.player:
                            message = '{} evaded your attack!'.format(creature.name)
                        elif creature.parent == GAME.player:
                            message = 'You evaded {} attack!'.format(self.name)
                            color = tcod.light_chartreuse
                        else:
                            message = '{} evaded {} attack!'.format(creature.name, self.name)
                        MESSAGE_LOG.add_message(message, color)
                else:
                    color = tcod.white
                    if self.parent == GAME.player:
                        message = 'You miss {}!'.format(creature.name)
                    elif creature.parent == GAME.player:
                        message = '{} misses you!'.format(self.name)
                        color = tcod.light_azure
                    else:
                        message = '{} misses {}!'.format(self.name, creature.name)
                    MESSAGE_LOG.add_message(message, color)

    def get_attacked(self, damage):
        evasion_rate = ((self.agility / 5) + (self.luck / 10)) * (0.75 + 0.5 * self.fatigue / self.max_fatigue)
        evaded = random.random() < evasion_rate / 100
        if not evaded:
            damage = int(damage / (1 + self.get_armor_rating() / damage))
            damage = self.take_damage(damage)
            death = False
            if self.health <= 0:
                self.die()
                death = True
            return damage, False, death
        else:
            return None, True, False

    def get_armor_rating(self):
        total_rating = 0
        for equipment in self.equipment.equipped:
            total_rating += equipment.armor_rating
        return total_rating

    def take_damage(self, damage):
        self.health -= damage
        return damage

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
