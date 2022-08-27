import queue
from vector import Vector

class Character:
    def __init__(self, pos = None, hp = 30, atk = 10, move_range = 1, atk_range = 1, speed=1):
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.move_range = move_range
        self.atk_range = atk_range
        self.pos = pos
        self.speed = speed

    def in_range(self, pos, _range):
        return pos - self.pos <= _range
    def can_move(self, new_pos):
        return self.in_range(new_pos, self.move_range)

    def can_attack(self, entity):
        return self.in_range(entity.pos, self.atk_range)

    def attack(self, other):
        if type(other) != Character:
            raise TypeError(f'invalid type {type(other)}')
        if not self.can_attack(other):
            raise Character.OutOfRange('character out of range')
        other.hp -= self.atk

    def move(self, pos):
        if not self.can_move(pos):
            raise Character.OutOfRange(f'{pos} out of move range')
        self.pos = pos 

    class OutOfRange(Exception): pass
    class DiagonalMovementError(Exception): pass

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.map = []
        for y in range(0, h):
            self.map.append([])
            for x in range(0, w):
                self.map[y].append('.')

    def __contains__(self, pos):
        return 0 <= pos.y <= len(self.map[0]) and 0 <= pos.x <= len(self.map[0])

    def __getitem__(self, key):
        return self.map[key]

    def __len__(self):
        return len(self.map)

class Entities:
    def __init__(self, entities: list):
        entities.sort(key=lambda e: e.speed, reverse=True)
        self.entities = entities

    def __getitem__(self, key):
        if type(key) == int:
            return self.entities[key]
        elif type(key) == Vector:
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

class FFT:
    def __init__(self, map_w, map_h, entities):
        self.entities = Entities(entities)
        self.map = Map(map_w, map_h)

    def move_entity(self, entity, new_pos):
        if not new_pos in self.map:
            raise FFT.PositionOutsideMap() 
        entity.move(new_pos)

    def attack_entity(self, attacker, attackee):
        attacker.attack(attackee)

    def take_turn(self, action, *args):
        entity = self.entities.next()
        if action == 'move':
            self.move_entity(entity, *args)
        elif action == 'attack':
            self.attack_entity(entity, *args)

    def __str__(self):
        string = ''
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.entities[Vector(y, x)]:
                    string += 'o/'
                elif self.entities[0].can_move(Vector(y, x)):
                    string += '# '
                else:
                    string += self.map[y][x]
                    string += ' '
            string += '\n'
        return string

    class PositionOutsideMap(Exception): pass
