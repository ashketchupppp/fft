import unittest
from fft import FFT
from character import Character
from map import Map
from vector import Vec

def getEntities():
    return [
        Character(Vec(0, 0), speed=2),
        Character(Vec(1, 1), speed=1)
    ]

def getGame(entities, w=10, h=10):
    return FFT(w, h, entities)

class TestFFT(unittest.TestCase):
    def test_move_entity(self):
        entities = getEntities()
        game = getGame(entities)
        new_pos = Vec(0, 1)
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
        new_pos = Vec(0, 2)
        with self.assertRaises(Character.OutOfRange):
            game.move_entity(game.entities[0], new_pos)

    def test_cannot_move_entity_outside_map(self):
        entities = getEntities()
        game = getGame(entities)
        with self.assertRaises(FFT.PositionOutsideMap):
            game.move_entity(entities[0], Vec(-10, -10))

    def test_take_turn(self):
        entities = getEntities()
        game = getGame(entities)
        c1 = game.entities[Vec(0, 0)]
        c2 = game.entities[Vec(1, 1)]
        self.assertEqual(c1, entities[0])
        self.assertEqual(c1, game.entities.peek_next())

        game.take_turn('move', Vec(1, 0))
        self.assertEqual(c2, game.entities.peek_next())
        self.assertEqual(game.entities[Vec(1, 0)], c1)
        game.take_turn('attack', c1)
        self.assertEqual(c1, game.entities.peek_next())
        self.assertEqual(c1.hp, c1.max_hp - c2.atk)

    def test_take_turn_throws_unavailable_action(self):
        entities = [
            Character(pos=Vec(0, 0), atk_range=1),
            Character(pos=Vec(10, 10), atk_range=100)
        ]
        game = getGame(entities)
        with self.assertRaises(FFT.UnavailableAction):
            game.take_turn('attack', entities[1])

    def test_available_actions(self):
        entities = [
            Character(pos=Vec(0, 0), atk_range=1),
            Character(pos=Vec(10, 10), atk_range=100)
        ]
        game = getGame(entities)
        self.assertEqual(game.available_actions(entities[0]), ['move'])
        self.assertEqual(game.available_actions(entities[1]), ['move', 'attack'])
         


class TestCharacter(unittest.TestCase):
    def test_attack(self):
        startingHp = 30
        c1 = Character(pos=Vec(0, 0))
        c2 = Character(hp=startingHp, pos=Vec(0, 1))
        c1.attack(c2)
        self.assertEqual(c2.hp, startingHp - c1.atk)

    def test_cannot_attack_out_of_range(self):
        c = Character(pos=Vec(0, 1), atk_range=1)
        inRangeChar = Character(pos=Vec(0, 0))
        outRangeChar = Character(pos=Vec(2, 2))
        c.attack(inRangeChar)
        with self.assertRaises(Character.OutOfRange):
            c.attack(outRangeChar)

    def test_can_move(self):
        testCharacter = Character(pos=Vec(0, 0))
        inRanges = [
            Vec(0, 0),
            Vec(1, 0),
            Vec(0, 1),
            Vec(-1, 0),
            Vec(0, -1)
        ]
        outRanges = [
            Vec(1, 1),
            Vec(2, 0),
            Vec(0, 2),
            Vec(-2, 0),
            Vec(0, -2)
        ]
        for vec in inRanges:
            self.assertTrue(testCharacter.can_move(vec))
        for vec in outRanges:
            self.assertFalse(testCharacter.can_move(vec))
    
    def test_cannot_move_diagonally(self):
        ranges = list(range(1, 4))
        testCharacter = Character(pos=Vec(0, 0), move_range=1)
        for r in ranges:
            testCharacter.move_range = r
            self.assertTrue(testCharacter.can_move(Vec(r - 1, r - 1)))            
            self.assertFalse(testCharacter.can_move(Vec(r, r)))
            self.assertFalse(testCharacter.can_move(Vec(r + 1, r + 1)))

class TestVec(unittest.TestCase):
    def test_less_than(self):
        self.assertTrue(Vec(0, 0) < Vec(0, 1))
        self.assertFalse(Vec(2, 2) < Vec(0, 1))
        self.assertTrue(Vec(0, 0) < 1)
        self.assertFalse(Vec(2, 2) < 2)

    def test_greater_than(self):
        self.assertFalse(Vec(0, 0) > Vec(0, 1))
        self.assertTrue(Vec(2, 2) > Vec(0, 1))
        self.assertFalse(Vec(0, 0) > 1)
        self.assertTrue(Vec(2, 2) > 2)

    def test_greater_than_or_equal_to(self):
        self.assertFalse(Vec(0, 0) >= Vec(0, 1))
        self.assertTrue(Vec(2, 2) >= Vec(0, 1))
        self.assertTrue(Vec(2, 2) >= Vec(2, 2))
        self.assertFalse(Vec(0, 0) >= 1)
        self.assertTrue(Vec(2, 2) >= 1)
        self.assertTrue(Vec(3, 3) >= 2)

    def test_less_than_or_equal_to(self):
        self.assertTrue(Vec(0, 0) <= Vec(0, 1))
        self.assertFalse(Vec(2, 2) <= Vec(0, 1))
        self.assertTrue(Vec(2, 2) <= Vec(2, 2))
        self.assertTrue(Vec(0, 0) <= 1)
        self.assertFalse(Vec(2, 2) <= 1)
        self.assertFalse(Vec(3, 3) <= 2)

if __name__ == '__main__':
    unittest.main()
