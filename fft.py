from vector import Vec
from map import Map

class Entities:
    def __init__(self, entities: list):
        entities.sort(key=lambda e: e.speed, reverse=True)
        self.entities = entities

    def __getitem__(self, key):
        if type(key) == int:
            return self.entities[key]
        elif type(key) == Vec:
            for e in self.entities:
                if e.pos == key:
                    return e

    def __len__(self):
        return len(self.entities)

    def peek_next(self):
        return self[0]

    def next(self):
        entity = self.entities[0]
        self.entities.remove(entity)
        self.entities.append(entity)
        return entity

    def kill(self, entity):
        self.entities.remove(entity)

class FFT:
    def __init__(self, map_w, map_h, entities: Entities):
        self.entities = Entities(entities)
        self.map = Map(map_w, map_h)

    def current_turns_entity(self):
        return self.entities.peek_next()

    def move_entity(self, entity, new_pos):
        if not new_pos in self.map:
            raise FFT.PositionOutsideMap() 
        entity.move(new_pos)

    def attack_entity(self, attacker, attackee):
        attacker.attack(attackee)
        if attackee.hp <= 0:
            self.entities.kill(attackee)

    def take_turn(self, action, *args):
        entity = self.entities.next()
        available_actions = self.available_actions(entity)
        if not action in available_actions:
            raise FFT.UnavailableAction
        if action == 'move':
            self.move_entity(entity, *args)
        elif action == 'attack':
            self.attack_entity(entity, *args)

    def entity_can_attack(self, entity):
        for i in range(len(self.entities)):
            if self.entities[i] != entity and entity.can_attack(self.entities[i]):
                return True

    def available_actions(self, entity):
        available_actions = []
        if 'move' in entity.actions:
            available_actions.append('move')
        if 'attack' in entity.actions and self.entity_can_attack(entity):
            available_actions.append('attack')

        return available_actions

    class PositionOutsideMap(Exception): pass
    class UnavailableAction(Exception): pass
