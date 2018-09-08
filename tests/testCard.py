import unittest
from card import Card
from colour import Colour


class TestCard(unittest.TestCase):

    def setUp(self):
        self.card = Card(Colour.RED, 10)

    def test_colour(self):
        self.assertEqual(self.card.colour, Colour.RED)

    def test_val(self):
        self.assertEqual(self.card.val, 10)

    def test_active(self):
        self.assertFalse(self.card.active)
        self.card.active = True
        self.assertTrue(self.card.active)


if __name__ == '__main__':
    unittest.main()
