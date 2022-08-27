import fft
from vector import Vector
entities = [
    fft.Character(Vector(4, 4), move_range=4, speed=2),
]
game = fft.FFT(10, 10, entities)
print(game)
