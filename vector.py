import math

def pythag(a, b):
    return math.sqrt(a**2 + b**2)

class Vec:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def dict(self):
        return vars(self)

    def copy(self):
        return Vec(self.x, self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        if type(other) == Vec:
            return self.x == other.x and self.y == other.y
        return False


    def __add__(self, other):
        if type(other) == int:
            return Vec(self.x + other, self.y + other)
        elif type(other) == Vec:
            return Vec(self.x + other.x, self.y + other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')

    def __sub__(self, other):
        if type(other) == int:
            return Vec(self.x - other, self.y - other)
        elif type(other) == Vec:
            return Vec(self.x - other.x, self.y - other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')

    def __lt__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) < other
        elif type(other) == Vec:
            return pythag(self.x, self.y) < pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')

    def __gt__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) > other
        elif type(other) == Vec:
            return pythag(self.x, self.y) > pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')

    def __le__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) <= other
        elif type(other) == Vec:
            return pythag(self.x, self.y) <= pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')

    def __ge__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) >= other
        elif type(other) == Vec:
            return pythag(self.x, self.y) >= pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vecor int')
