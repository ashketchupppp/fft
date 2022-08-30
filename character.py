import numpy as np

class Character:
    def __init__(self, pos = None, hp = 30, atk = 10, move_range = 1, atk_range = 1, speed=1, team=0):
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.move_range = move_range
        self.atk_range = atk_range
        self.pos = pos
        self.speed = speed
        self.team = team
        self.actions = [
            'move',
            'attack',
            'wait'
        ]

    def in_range(self, to_pos, _range, from_pos=None):
        if from_pos == None:
            from_pos = self.pos
        return to_pos - from_pos <= _range

    def can_move_to(self, new_pos, from_pos=None):
        if from_pos == None:
            from_pos = self.pos
        return self.in_range(new_pos, self.move_range, from_pos)

    def can_attack(self, entity, from_pos = None):
        if not from_pos:
            from_pos = self.pos
        return self.in_range(entity.pos, self.atk_range, from_pos) and self.team != entity.team

    def attack(self, other):
        if type(other) != Character:
            raise TypeError(f'invalid type {type(other)}')
        if not self.can_attack(other):
            raise Character.CannotAttack()
        other.hp -= self.atk

    def move(self, pos):
        if not self.can_move_to(pos):
            raise Character.CannotMove(f'{pos} out of move range')
        self.pos = pos 

    def encode(self):
        return np.array([
            self.hp,
            self.atk,
            self.pos.x,
            self.pos.y,
            self.team
        ])
        


    class CannotAttack(Exception): pass
    class CannotMove(Exception): pass