import unittest

import ui
from fft import FFT
from character import Character
from vector import Vec

def getEntities():
    return [
        Character(Vec(0, 0), speed=2),
        Character(Vec(1, 1), speed=1)
    ]

def getGame(entities, w=10, h=10):
    return FFT(w, h, entities)

class TestUI(unittest.TestCase):
    def test_draw_map(self):
        entities = getEntities()
        game = getGame(entities)
        map = ui.draw_map(game)

if __name__ == '__main__':
    unittest.main()