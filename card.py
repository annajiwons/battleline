from colour import Colour
import random


class Card:

    def __init__(self, colour, val):
        self._colour = colour
        self._val = val
        # Active means the card is in a player's hand or in a slot
        self._active = False

    @property
    def colour(self):
        return self._colour

    @property
    def val(self):
        return self._val

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, state):
        self._active = state


class CardManager:
    # Instance of CardManager
    __instance = None
    _card_dict = {}

    # Static access method
    @staticmethod
    def get_instance():
        if CardManager.__instance is None:
            CardManager()
        return CardManager.__instance

    def __init__(self):
        if CardManager.__instance is not None:
            raise Exception("Class is singleton")
        else:
            CardManager.__instance = self

    @property
    def card_dict(self):
        return self._card_dict

    # Get card with given key if it exists in CardManager,
    # creating it and adding it to the CardManger if needed.
    # The key is a string made of the colour's enum value + the card number.
    # Throw ValueError if colour val or number is invalid.
    def get_card(self, card_key):
        if card_key in self._card_dict:
            return self._card_dict[card_key]

        colour_val = int(card_key[0:1])
        number = int(card_key[1:])

        if colour_val < 1 or colour_val > 6:
            raise ValueError("Invalid colour val", colour_val)

        if number < 1 or number > 10:
            raise ValueError("Invalid card number", number)

        new_card = Card(Colour(colour_val), number)
        self._card_dict[card_key] = new_card
        return new_card

    def get_num_cards(self):
        return len(self._card_dict)

    def get_num_inactive_cards(self):
        active_cards = []
        for key in self._card_dict:
            card = self._card_dict[key]
            if not card.active:
                active_cards.append(card)
        return len(active_cards)

    def clear_cards(self):
        self._card_dict.clear()

    # Pick a given number of random inactive cards and return a list of them.
    # If there are less than number of cards in the dict, raise ValueError
    def pick_random_inactive_cards(self, number):
        if number > self.get_num_inactive_cards():
            raise ValueError("There are not enough cards", self.get_num_cards())

        list_random = []
        i = 0
        while i < number:
            card = self.pick_random_card()
            if card not in list_random and not card.active:
                card.active = True
                list_random.append(card)
                i += 1
        return list_random

    # Picks a random card and returns it
    def pick_random_card(self):
        return random.choice(list(self._card_dict.values()))

    # Load all cards needed for the game i.e. load ten cards of each colour
    def load_all_cards(self):
        for i in range(1, 11):
            for j in range(1, 7):
                self.get_card(str(j) + str(i))
