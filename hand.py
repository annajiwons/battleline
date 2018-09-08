class Hand:

    # Create a hand with an empty list of cards and the given hand number.
    # Hand number can either be 1 or 2
    def __init__(self, hand_no):
        if hand_no > 2 or hand_no < 1:
            raise ValueError('Hand no can either be 1 or 2')
        self._cards = []
        self._hand_no = hand_no

    @property
    def cards(self):
        return self._cards

    @property
    def hand_no(self):
        return self._hand_no

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.cards.append(card)

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)


class Slot:

    def __init__(self):
        self._p1_played = []
        self._p2_played = []
        self._winner = 0

    @property
    def p1_played(self):
        return self._p1_played

    @property
    def p2_played(self):
        return self._p2_played

    @property
    def winner(self):
        return self._winner

    # Add given card to slot on given hand's side if the card belongs to
    # that hand.
    # Raise ValueError if the card does not belong to the given hand.
    def play_card(self, card, hand):

        if hand.hand_no == 1:
            played_list = self._p1_played
        else:
            played_list = self._p2_played

        if self.check_card_belongs_to_player(card, hand):
            played_list.append(card)
            hand.remove_card(card)
        else:
            raise ValueError('Invalid play')

    def check_card_belongs_to_player(self, card, hand):
        return card in hand.cards

    # Checks if there is a winner for this slot, sets winner to the player_no of
    # the player that won, and returns that player_no.
    # If there is no winner yet, return 0.
    # Slots is the other slots in the game.
    def check_winner(self, slots):
        p1_has = len(self._p1_played)
        p2_has = len(self._p2_played)

        # If neither side is full, winner cannot be determined
        if p1_has != 3 and p2_has != 3:
            return 0

        # If one of the sides has just one card, don't determine winner
        if p1_has == 1 or p2_has == 1:
            return 0

        if p1_has == 3 and p2_has == 3:
            self._winner = self.check_winner_full_sides()
            return self._winner

        elif p1_has == 2 or p2_has == 2:
            self._winner = self.check_winner_two_on_one_side(slots)
            return self._winner

    # If both sides are full, winner is determined by formation score. If the formation
    # score is the same, it is determined by the sum of the card values.
    def check_winner_full_sides(self):
        p1_score = self.get_formation_score(self._p1_played)
        p2_score = self.get_formation_score(self._p2_played)
        p1_sum = self.sum_card_values(self._p1_played)
        p2_sum = self.sum_card_values(self._p2_played)
        if p1_score > p2_score:
            return 1
        elif p1_score == p2_score:
            if p1_sum > p2_sum:
                return 1
            elif p1_sum == p2_sum:
                return 0
            else:
                return 2
        else:
            return 2

    # If one side has 2 cards and the other side has 3 cards, first check if the
    # side with 2 cards can have a higher formation score. If it can, then check if it
    # is possible to beat the full side. If the side with 2 cards can ONLY get the same score and sum
    # as the side with 3 cards, the side with 3 cards wins because it got it first.
    def check_winner_two_on_one_side(self, slots):
        p1_has = len(self._p1_played)
        player_full_cards = self._p1_played if p1_has == 3 else self._p2_played
        player_not_full_cards = self._p1_played if p1_has == 2 else self._p2_played
        player_full_score = self.get_formation_score(player_full_cards)
        player_not_full_score = self.get_highest_pos_formation_score(player_not_full_cards)
        if player_full_score > player_not_full_score:
            if player_full_cards == self._p1_played:
                return 1
            else:
                return 2
        elif player_full_score == player_not_full_score:
            if player_full_score == 1:
                return self.who_wins_host(player_full_cards, player_not_full_cards, slots)
            elif self.can_two_side_win_equal_or_less_formation(player_not_full_score,
                                                             player_full_cards, player_not_full_cards, slots):
                return 0
            else:
                if player_full_cards == self._p1_played:
                    return 1
                else:
                    return 2
        elif player_full_score < player_not_full_score:
            if self.can_two_side_win_equal_or_less_formation(player_not_full_score,
                                                             player_full_cards, player_not_full_cards, slots):
                return 0
            else:
                # If the highest possible formation score for the not full side was 5, then
                # it may still form a battalion order, which could be higher than player_full_score.
                if player_not_full_score == 5 and player_full_score <= 3:
                    if self.can_two_side_win_equal_or_less_formation(3, player_full_cards, player_full_cards, slots):
                        return 0
                if player_full_cards == self._p1_played:
                    return 1
                else:
                    return 2

    # Determines who wins in the case that they are both hosts.
    def who_wins_host(self, player_full_cards, player_not_full_cards, slots):
        sum_full_cards = self.sum_card_values(player_full_cards)
        sum_of_two_cards = self.sum_card_values(player_not_full_cards)
        if sum_of_two_cards >= sum_full_cards:
            if player_not_full_cards == self._p1_played:
                return 1
            else:
                return 2
        else:
            diff = sum_full_cards - sum_of_two_cards
            if diff >= 10:
                if player_full_cards == self._p1_played:
                    return 1
                else:
                    return 2
            else:
                for i in range(diff, 10):
                    if not self.are_all_cards_of_this_val_out(i, slots):
                        return 0

    # Returns true if the side with two cards may win in the future. That is: if it is possible to get
    # the formation corresponding to score_of_not_full using cards that are not already in the given
    # slots, and have the score and sum of cards be larger than score_of_full.
    # Does not include host which is checked earlier.
    # Assume the formation score of the side with two cards as equal or less to that of the full side.
    def can_two_side_win_equal_or_less_formation(self, player_not_full_score, player_full_cards,
                                                 player_not_full_cards, slots):
        can_complete = False
        # This is the highest value that is still not out that can be used to complete a formation.
        highest_value_card_needed_and_not_played = 0

        # Hedge can be completed if there are still cards that can form consecutive values
        # of the same colour not yet out.
        if player_not_full_score == 5:
            values_needed = self.get_values_to_complete_consecutive(player_not_full_cards)
            value_needed_1 = values_needed[0]
            is_card_1_out = self.is_this_card_out(value_needed_1, player_not_full_cards[0].colour, slots)
            # If there is only one value possible to complete hedge, it can be completed if card 1 isn't out.
            if len(values_needed) == 1:
                highest_value_card_needed_and_not_played = value_needed_1
                can_complete = not is_card_1_out
            # If there are two values possible to complete hedge, it can be completed if either card 1 or 2 isn't out.
            elif len(values_needed) == 2:
                value_needed_2 = values_needed[1]
                is_card_2_out = self.is_this_card_out(value_needed_2, player_not_full_cards[0].colour, slots)
                if not is_card_1_out:
                    if is_card_2_out:
                        highest_value_card_needed_and_not_played = value_needed_1
                        can_complete = True
                    else:
                        highest_value_card_needed_and_not_played = max(value_needed_1, value_needed_2)
                        can_complete = True
                elif not is_card_2_out:
                    highest_value_card_needed_and_not_played = value_needed_2
                    can_complete = True

        # Phalanx can be completed if there are still cards with the value not yet out.
        elif player_not_full_score == 4:
            are_all_cards_of_val_out = self.are_all_cards_of_this_val_out(player_not_full_cards[0].val, slots)
            if not are_all_cards_of_val_out:
                highest_value_card_needed_and_not_played = player_not_full_cards[0].val
                can_complete = True

        # Battalion Order can be completed if there are still cards with the colour not yet out.
        elif player_not_full_score == 3:
            are_all_cards_of_colour_out = self.are_all_cards_of_this_colour_out(player_not_full_cards[0].colour, slots)
            if not are_all_cards_of_colour_out:
                highest_value_card_needed_and_not_played = self.get_highest_card_with_colour_not_played \
                    (player_not_full_cards[0].colour, slots)
                can_complete = True

        # Skirmish Line can be completed if there are still cards that can form consecutive values.
        elif player_not_full_score == 2:
            values_needed = self.get_values_to_complete_consecutive(player_not_full_cards)
            for value in values_needed:
                if not self.are_all_cards_of_this_val_out(value, slots):
                    highest_value_card_needed_and_not_played = value
                    can_complete = True

        return can_complete and (highest_value_card_needed_and_not_played + self.sum_card_values(player_not_full_cards)
                                 > self.sum_card_values(player_full_cards))

    def get_values_to_complete_consecutive(self, cards):
        sorted_cards = self.sort_by_val(cards)
        if sorted_cards[1].val - sorted_cards[0].val == 1:
            if sorted_cards[0].val == 1:
                return [sorted_cards[1].val + 1]
            if sorted_cards[1].val == 10:
                return [sorted_cards[0].val - 1]
            else:
                return [sorted_cards[0].val - 1, sorted_cards[1].val + 1]
        else:
            return [sorted_cards[0].val + 1]

    # Returns true if given card is in the given slots.
    def is_this_card_out(self, value, colour, slots):
        for slot in slots:
            for card in slot.p1_played:
                if card.val == value and card.colour == colour:
                    return True
            for card in slot.p2_played:
                if card.val == value and card.colour == colour:
                    return True
        return False

    # Returns true if all cards of a given value (6 cards per value) are in the given slots.
    def are_all_cards_of_this_val_out(self, value, slots):
        count = 0
        for slot in slots:
            for card in slot.p1_played:
                if card.val == value:
                    count += 1
            for card in slot.p2_played:
                if card.val == value:
                    count += 1
        return count >= 6

    # Returns true if all cards of a given colour (10 cards per colour) are in the given slots.
    def are_all_cards_of_this_colour_out(self, colour, slots):
        count = 0
        for slot in slots:
            for card in slot.p1_played:
                if card.colour == colour:
                    count += 1
            for card in slot.p2_played:
                if card.colour == colour:
                    count += 1
        return count >= 6

    # Get the formation score for a list of cards.
    # Hedge: 3 same colour consecutive cards (5 points)
    # Phalanx: 3 cards of same value (4 points)
    # Battalion order: 3 cards of same colour (3 points)
    # Skirmish line: 3 cards with consecutive values (2 points)
    # Host: any 3 cards (1 point)
    def get_formation_score(self, cards):
        sorted_cards = self.sort_by_val(cards)
        if self.has_cons_values(sorted_cards):
            if self.has_same_colours(sorted_cards):
                return 5
            else:
                return 2
        elif self.has_same_values(sorted_cards):
            return 4
        elif self.has_same_colours(sorted_cards):
            return 3
        else:
            return 1

    # Get the highest possible formation score for a list of 2 cards.
    def get_highest_pos_formation_score(self, cards):
        sorted_cards = self.sort_by_val(cards)
        if self.maybe_cons_values(sorted_cards):
            if self.has_same_colours(sorted_cards):
                return 5
            else:
                return 2
        elif self.has_same_values(sorted_cards):
            return 4
        elif self.has_same_colours(sorted_cards):
            return 3
        else:
            return 1

    # Get the value of the highest card with the given colour that is not in the given slots.
    def get_highest_card_with_colour_not_played(self, colour, slots):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for slot in slots:
            for card in slot.p1_played:
                if card.colour == colour:
                    values.remove(card.val)
            for card in slot.p2_played:
                if card.colour == colour:
                    values.remove(card.val)
        return max(values)

    # Get the sum of the card values.
    def sum_card_values(self, cards):
        sum = 0
        for card in cards:
            sum += card.val
        return sum

    # Sort cards by value
    def sort_by_val(self, cards):
        return sorted(cards, key=self.get_card_val)

    # Custom key function for sorting
    def get_card_val(self, card):
        return card.val

    # Returns true if the cards in the list all have the same colour and false otherwise.
    def has_same_colours(self, cards):
        col = cards[0].colour
        for card in cards[1:]:
            if card.colour != col:
                return False
        return True

    # Returns true if the cards in the list have consecutive values and false otherwise.
    # Assume cards are sorted by value.
    def has_cons_values(self, cards):
        prev = cards[0].val
        for card in cards[1:]:
            if card.val - prev != 1:
                return False
            else:
                prev = card.val
        return True

    # For two cards, returns true if the cards could have consecutive values
    # i.e. they have a difference of either 1 or 2
    def maybe_cons_values(self, cards):
        prev = cards[0].val
        for card in cards[1:]:
            if (card.val - prev != 1) and (card.val - prev != 2):
                return False
            else:
                prev = card.val
        return True

    # Returns true if the cards in the list all have the same value and false otherwise.
    def has_same_values(self, cards):
        val = cards[0].val
        for card in cards[1:]:
            if card.val != val:
                return False
        return True
