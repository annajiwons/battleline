import unittest
from card import CardManager
from colour import Colour


class TestCardManager(unittest.TestCase):

    def setUp(self):
        self.card_manager = CardManager.get_instance()
        CardManager.get_instance()
        self.card_manager.clear_cards()

    def test_add_new_cards(self):
        cards = self.card_manager
        self.assertEqual(cards.get_card('110').colour, Colour.RED)
        self.assertEqual(cards.get_card('110').val, 10)
        self.assertEqual(cards.get_card('52').colour, Colour.BLUE)
        self.assertEqual(cards.get_card('52').val, 2)
        self.assertEqual(cards.get_num_cards(), 2)

    def test_add_invalid_cards(self):
        try:
            self.card_manager.get_card('710')
            self.fail('ValueError not thrown')
        except ValueError as err:
            self.assertEqual(err.args[1], 7)

        try:
            self.card_manager.get_card('280')
            self.fail('ValueError not thrown')
        except ValueError as err:
            self.assertEqual(err.args[1], 80)

    def test_clear_cards(self):
        cards = self.card_manager
        cards.get_card('110')
        cards.get_card('52')
        self.assertEqual(cards.get_num_cards(), 2)
        cards.clear_cards()
        self.assertEqual(cards.get_num_cards(), 0)

    def test_pick_random_card(self):
        self.card_manager.load_all_cards()
        card = self.card_manager.pick_random_card()
        print(card.colour.name + str(card.val))

    def test_pick_random_inactive_cards(self):
        self.card_manager.load_all_cards()
        cards = self.card_manager.pick_random_inactive_cards(10)
        self.assertEqual(len(cards), 10)
        for i in range(0, len(cards)):
            self.assertTrue(cards[i].active)
            print(cards[i].colour.name + str(cards[i].val))

    def test_pick_random_inactive_cards_no_more_cards(self):
        self.card_manager.load_all_cards()
        cards = self.card_manager.pick_random_inactive_cards(60)
        try:
            more_cards = self.card_manager.pick_random_inactive_cards(1)
            self.fail('ValueError not thrown')
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main()
