import unittest
from hand import Hand
from card import Card
from colour import Colour


class TestHand(unittest.TestCase):

    def setUp(self):
        self.hand_1 = Hand(1)
        self.hand_2 = Hand(2)

    def test_add(self):
        c1 = Card(Colour.RED, 10)
        c2 = Card(Colour.BLUE, 1)
        c3 = Card(Colour.GREEN, 5)
        self.hand_1.add_card(c1)
        self.hand_1.add_card(c2)
        self.hand_1.add_card(c3)
        self.assertTrue(c1 in self.hand_1.cards)
        self.assertTrue(c2 in self.hand_1.cards)
        self.assertTrue(c3 in self.hand_1.cards)

    def test_add_many(self):
        c1 = Card(Colour.RED, 10)
        c2 = Card(Colour.BLUE, 1)
        c3 = Card(Colour.GREEN, 5)
        l = [c1, c2, c3]
        self.hand_1.add_cards(l)
        self.assertTrue(c1 in self.hand_1.cards)
        self.assertTrue(c2 in self.hand_1.cards)
        self.assertTrue(c3 in self.hand_1.cards)

    def test_remove(self):
        c1 = Card(Colour.RED, 10)
        c2 = Card(Colour.BLUE, 1)
        c3 = Card(Colour.GREEN, 5)
        self.hand_1.add_card(c1)
        self.hand_1.add_card(c2)
        self.hand_1.add_card(c3)
        self.hand_1.remove_card(c1)
        self.assertFalse(c1 in self.hand_1.cards)
        self.assertTrue(c2 in self.hand_1.cards)
        self.assertTrue(c3 in self.hand_1.cards)

    def test_remove_card_not_in_hand(self):
        c1 = Card(Colour.RED, 10)
        c2 = Card(Colour.BLUE, 1)
        c3 = Card(Colour.GREEN, 5)
        self.hand_1.add_card(c1)
        self.hand_1.add_card(c2)
        self.hand_1.remove_card(c3)
        self.assertTrue(c1 in self.hand_1.cards)
        self.assertTrue(c2 in self.hand_1.cards)
        self.assertFalse(c3 in self.hand_1.cards)


if __name__ == '__main__':
    unittest.main()
