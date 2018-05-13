from enum import Enum


class CreatureEquipment:
    def __init__(self):
        self.equipped = list()

    def get_slots_status(self):
        slots = {slot: None for slot in EquipmentSlots}
        for item in self.equipped:
            for slot in item.taken_slots:
                slots[slot] = item
        return slots

    def equip(self, item, slot):
        slot_group = item.get_slot_group_with_slot(slot)
        self.unequip_slots(slot_group)
        item.equip(slot)
        self.equipped.append(item)

    def unequip(self, item):
        item.unequip()
        self.equipped.remove(item)

    def unequip_slots(self, slots):
        slot_status = self.get_slots_status()
        for slot in slots:
            item = slot_status[slot]
            if item:
                item.unequip()
                self.equipped.remove(item)


class Item:
    def __init__(self, name, object_id):
        self.name = name
        self.object_id = object_id
        self.type = ItemType.ITEM


class Equipment(Item):
    def __init__(self, name, object_id, possible_slots):
        super().__init__(name, object_id)
        # List of EquipmentSlots groups which can be simultaneously occupied by this piece of equipment
        self.possible_slots = possible_slots
        # List of EquipmentSlots currently occupied
        self.taken_slots = None
        self.type = ItemType.EQUIPMENT

    def get_slot_group_with_slot(self, slot):
        for slot_group in self.possible_slots:
            if slot in slot_group:
                return slot_group

    def equip(self, slot):
        self.taken_slots = self.get_slot_group_with_slot(slot)

    def unequip(self):
        self.taken_slots = None


class Weapon(Equipment):
    def __init__(self, name, object_id, base_damage, two_handed=False):
        possible_slots = [
            [EquipmentSlots.LEFT_HAND],
            [EquipmentSlots.RIGHT_HAND]
        ] if not two_handed else [
            [EquipmentSlots.LEFT_HAND, EquipmentSlots.RIGHT_HAND]
        ]
        super().__init__(name, object_id, possible_slots)
        self.base_damage = base_damage
        self.type = ItemType.WEAPON

    @property
    def damage(self):
        return self.base_damage


class EquipmentSlots(Enum):
    BODY = 'body'
    LEGS = 'legs'
    HANDS = 'hands'
    HEAD = 'head'
    NECK = 'neck'
    LEFT_RING = 'left_ring'
    RIGHT_RING = 'right_ring'
    LEFT_HAND = 'left_hand'
    RIGHT_HAND = 'right_hand'


class ItemType(Enum):
    ITEM = 'item'
    EQUIPMENT = 'equipment'
    WEAPON = 'weapon'
