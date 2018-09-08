
def print_cards(cards):
    for card in cards:
        print_card(card)


def print_card(card):
    print(card.colour.name + str(card.val))