import numpy as np

from character import Character
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
    
    def __iter__(self):
        for e in self.entities:
            yield e

    def __len__(self):
        return len(self.entities)

    def encode(self):
        return np.concatenate([entity.encode() for entity in self.entities])

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
        self.turn_num = 0

    def current_turns_entity(self) -> Character:
        return self.entities.peek_next()

    def move_entity(self, entity, new_pos):
        if not new_pos in self.map:
            raise FFT.PositionOutsideMap() 
        entity.move(new_pos)

    def attack_entity(self, attacker, attackee):
        attacker.attack(attackee)
        if attackee.hp <= 0:
            self.entities.kill(attackee)

    def take_turn(self, *actions):
        if len(actions) > 2:
            raise FFT.TooManyActions

        entity = self.entities.peek_next()
        available_actions = self.available_actions(entity)
        to_perform = []

        # first action can be move, attack or wait, any action
        first_action_name, first_action_arg = actions[0]
        if not first_action_name in available_actions:
            raise FFT.UnavailableAction
        to_perform.append(actions[0])

        if len(actions) > 1:
            # second action can be attack or wait if the first one was move
            if first_action_name != 'move':
                raise FFT.TooManyActions

            # first action was move, so re-calculate entities actions from their proposed pos
            second_action_name, _ = actions[1]
            from_pos = entity.pos + first_action_arg
            available_actions = self.available_actions(entity, from_pos=from_pos)
            available_actions.remove('move')

            if not second_action_name in available_actions:
                raise FFT.UnavailableAction

            to_perform.append(actions[1])

        for action in to_perform:
            name, arg = action
            if name == 'move':
                self.move_entity(entity, arg)
            elif name == 'attack':
                self.attack_entity(entity, arg)
            elif name == 'wait':
                pass
            else:
                raise FFT.UnknownAction(name)
        self.entities.next()
        self.turn_num += 1

    def entity_can_attack(self, entity, from_pos):
        if not from_pos:
            from_pos = entity.pos

        for i in range(len(self.entities)):
            if self.entities[i] != entity and entity.can_attack(self.entities[i], from_pos):
                return True

    def available_actions(self, entity, from_pos = None):
        can_attack = self.entity_can_attack(entity, from_pos)

        available_actions = ['wait']
        if 'move' in entity.actions:
            available_actions.append('move')
        if 'attack' in entity.actions and can_attack:
            available_actions.append('attack')

        return available_actions

    def encode(self):
        return self.entities.encode()

    class PositionOutsideMap(Exception): pass
    class UnavailableAction(Exception): pass
    class TooManyActions(Exception): pass
    class UnknownAction(Exception): pass