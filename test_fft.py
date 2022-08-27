import unittest
import fft
from vector import Vector

def getEntities():
    return [
        fft.Character(Vector(0, 0), speed=2),
        fft.Character(Vector(1, 1), speed=1)
    ]

def getGame(entities, w=10, h=10):
    return fft.FFT(w, h, entities)

class TestFFT(unittest.TestCase):
    def test_move_entity(self):
        entities = getEntities()
        game = getGame(entities)
        new_pos = Vector(0, 1)
        game.move_entity(entities[0], new_pos)
        self.assertEqual(entities[0].pos, new_pos)

        # entity list should initially be sorted by character speed
        prevEntity = game.entities.next()
        for i in range(1, len(game.entities)):
            current = game.entities.next()
            self.assertTrue(current.speed <= prevEntity.speed)
            prevEntity = current

    def test_cannot_move_entity_outside_move_range(self):
        entities = getEntities()
        game = getGame(entities)
        new_pos = Vector(0, 2)
        with self.assertRaises(fft.Character.OutOfRange):
            game.move_entity(game.entities[0], new_pos)

    def test_cannot_move_entity_outside_map(self):
        entities = getEntities()
        game = getGame(entities)
        with self.assertRaises(fft.FFT.PositionOutsideMap):
            game.move_entity(entities[0], Vector(-10, -10))

    def test_take_turn(self):
        entities = getEntities()
        game = getGame(entities)
        c1 = game.entities[Vector(0, 0)]
        c2 = game.entities[Vector(1, 1)]
        self.assertEqual(c1, entities[0])
        self.assertEqual(c1, game.entities.peek_next())

        game.take_turn('move', Vector(1, 0))
        self.assertEqual(c2, game.entities.peek_next())
        self.assertEqual(game.entities[Vector(1, 0)], c1)
        game.take_turn('attack', c1)
        self.assertEqual(c1, game.entities.peek_next())
        self.assertEqual(c1.hp, c1.max_hp - c2.atk)


class TestCharacter(unittest.TestCase):
    def test_attack(self):
        startingHp = 30
        c1 = fft.Character(pos=Vector(0, 0))
        c2 = fft.Character(hp=startingHp, pos=Vector(0, 1))
        c1.attack(c2)
        self.assertEqual(c2.hp, startingHp - c1.atk)

    def test_cannot_attack_out_of_range(self):
        c = fft.Character(pos=Vector(0, 1), atk_range=1)
        inRangeChar = fft.Character(pos=Vector(0, 0))
        outRangeChar = fft.Character(pos=Vector(2, 2))
        c.attack(inRangeChar)
        with self.assertRaises(fft.Character.OutOfRange):
            c.attack(outRangeChar)

    def test_can_move(self):
        testCharacter = fft.Character(pos=Vector(0, 0))
        inRanges = [
            Vector(0, 0),
            Vector(1, 0),
            Vector(0, 1),
            Vector(-1, 0),
            Vector(0, -1)
        ]
        outRanges = [
            Vector(1, 1),
            Vector(2, 0),
            Vector(0, 2),
            Vector(-2, 0),
            Vector(0, -2)
        ]
        for vec in inRanges:
            self.assertTrue(testCharacter.can_move(vec))
        for vec in outRanges:
            self.assertFalse(testCharacter.can_move(vec))
    
    def test_cannot_move_diagonally(self):
        ranges = list(range(1, 4))
        testCharacter = fft.Character(pos=Vector(0, 0), move_range=1)
        for r in ranges:
            testCharacter.move_range = r
            self.assertTrue(testCharacter.can_move(Vector(r - 1, r - 1)))            
            self.assertFalse(testCharacter.can_move(Vector(r, r)))
            self.assertFalse(testCharacter.can_move(Vector(r + 1, r + 1)))

class TestVector(unittest.TestCase):
    def test_less_than(self):
        self.assertTrue(Vector(0, 0) < Vector(0, 1))
        self.assertFalse(Vector(2, 2) < Vector(0, 1))
        self.assertTrue(Vector(0, 0) < 1)
        self.assertFalse(Vector(2, 2) < 2)

    def test_greater_than(self):
        self.assertFalse(Vector(0, 0) > Vector(0, 1))
        self.assertTrue(Vector(2, 2) > Vector(0, 1))
        self.assertFalse(Vector(0, 0) > 1)
        self.assertTrue(Vector(2, 2) > 2)

    def test_greater_than_or_equal_to(self):
        self.assertFalse(Vector(0, 0) >= Vector(0, 1))
        self.assertTrue(Vector(2, 2) >= Vector(0, 1))
        self.assertTrue(Vector(2, 2) >= Vector(2, 2))
        self.assertFalse(Vector(0, 0) >= 1)
        self.assertTrue(Vector(2, 2) >= 1)
        self.assertTrue(Vector(3, 3) >= 2)

    def test_less_than_or_equal_to(self):
        self.assertTrue(Vector(0, 0) <= Vector(0, 1))
        self.assertFalse(Vector(2, 2) <= Vector(0, 1))
        self.assertTrue(Vector(2, 2) <= Vector(2, 2))
        self.assertTrue(Vector(0, 0) <= 1)
        self.assertFalse(Vector(2, 2) <= 1)
        self.assertFalse(Vector(3, 3) <= 2)

if __name__ == '__main__':
    unittest.main()
