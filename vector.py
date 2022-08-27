import math

def pythag(a, b):
    return math.sqrt(a**2 + b**2)

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        if type(other) == Vector:
            return self.x == other.x and self.y == other.y
        return self == other


    def __add__(self, other):
        if type(other) == int:
            return Vector(self.x + other, self.y + other)
        elif type(other) == Vector:
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')

    def __sub__(self, other):
        if type(other) == int:
            return Vector(self.x - other, self.y - other)
        elif type(other) == Vector:
            return Vector(self.x - other.x, self.y - other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')

    def __lt__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) < other
        elif type(other) == Vector:
            return pythag(self.x, self.y) < pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')

    def __gt__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) > other
        elif type(other) == Vector:
            return pythag(self.x, self.y) > pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')

    def __le__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) <= other
        elif type(other) == Vector:
            return pythag(self.x, self.y) <= pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')

    def __ge__(self, other):
        if type(other) == int:
            return pythag(self.x, self.y) >= other
        elif type(other) == Vector:
            return pythag(self.x, self.y) >= pythag(other.x, other.y)
        raise TypeError(f'invalid type: {type(other)}, not Vector or int')
