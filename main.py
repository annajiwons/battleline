import pygame
from card import CardManager, Card
from colour import Colour
from hand import Hand, Slot
import debug_util


class App:
    GAMECARD_SIZE = [40, 50]
    P1_Y_VAL = 400
    P2_Y_VAL = 40
    SLOTS_Y_VAL = 220

    def __init__(self):
        self._running = True
        # Display surface for game
        self._display_surf = None
        self.size = self.weight, self.height = 640, 500

        # Game objects
        self._game_cards_1 = []
        self._game_cards_2 = []
        self._game_slots = []

        # Hand objects
        self._h1 = None
        self._h2 = None

        self._clicked = []
        self._turn = 1

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._display_surf.fill((250, 250, 250))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._clicked.clear()
            pos = pygame.mouse.get_pos()
            if self._turn == 1:
                clicked_cards = [o for o in self._game_cards_1 if o.rect.collidepoint(pos)]
            else:
                clicked_cards = [o for o in self._game_cards_2 if o.rect.collidepoint(pos)]
            self._clicked.extend(clicked_cards)

        if event.type == pygame.MOUSEBUTTONUP:
            curr_hand = self._h1 if self._turn == 1 else self._h2
            game_cards = self._game_cards_1 if self._turn == 1 else self._game_cards_2
            pos = pygame.mouse.get_pos()
            released_on_slots = [o for o in self._game_slots if o.rect.collidepoint(pos)]
            if len(self._clicked) != 0 and len(released_on_slots) != 0:
                game_slot = released_on_slots[0]
                if (self._turn == 1 and len(game_slot.slot.p1_played) < 3) or \
                        (self._turn == 2 and len(game_slot.slot.p2_played) < 3):
                    x, y = self._clicked[0].pos
                    game_slot.handle_release(game_cards, self._clicked[0], curr_hand, self._game_slots)
                    self.draw_card(x, y)
                    self._clicked.clear()
                    self.change_turn()
            debug_util.print_cards(o.card for o in self._game_cards_1)
            debug_util.print_cards(o.card for o in self._game_cards_2)

    def draw_card(self, x , y):
        hand = self._h1 if self._turn == 1 else self._h2
        print("x pos of new card: " + str(x))
        print("y pos of new card: " + str(y))
        try:
            new_cards = CardManager.get_instance().pick_random_inactive_cards(1)
            new_card = new_cards[0]
            hand.add_card(new_card)

            game_cards = self._game_cards_1 if self._turn == 1 else self._game_cards_2
            game_cards.append(self.load_game_card(new_card, x, y))
        except ValueError:
            print('no more cards to draw')

    def change_turn(self):
        self._turn = 1 if self._turn == 2 else 2

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.fill((250, 250, 250))
        self.render_turn()
        if self._turn == 1:
            for obj in self._game_cards_1:
                obj.render(self._display_surf)
        else:
            for obj in self._game_cards_2:
                obj.render(self._display_surf)
        for obj in self._game_slots:
            obj.render(self._display_surf)
        pygame.display.update()

    def render_turn(self):
        turn_font = pygame.font.SysFont('Helvetica Neue', 40)
        turn_surface = pygame.Surface([40, 50])
        pygame.draw.rect(turn_surface, (250, 250, 250), (0, 0, 40, 50))
        if self._turn == 1:
            turn_surface.blit(turn_font.render(str(self._turn), True, (244, 146, 162)),
                              [5, 10])
        else:
            turn_surface.blit(turn_font.render(str(self._turn), True, (160, 244, 200)),
                              [5, 10])
        self._display_surf.blit(turn_surface, (0, 0))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        self.load_game_objects()

        # Game loop
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def load_game_objects(self):
        # Load Cards
        cm = CardManager.get_instance()
        cm.load_all_cards()
        # Load two Hands and add 7 starting cards to them
        self._h1 = Hand(1)
        self._h2 = Hand(2)
        self._h1.add_cards(cm.pick_random_inactive_cards(7))
        self._h2.add_cards(cm.pick_random_inactive_cards(7))
        # Load GameCards
        self._game_cards_1.extend(self.load_game_cards_for_hand(self._h1, self.P1_Y_VAL))
        self._game_cards_2.extend(self.load_game_cards_for_hand(self._h2, self.P2_Y_VAL))
        # Load Slots
        slots = [Slot() for i in range(9)]
        # Load GameSlots
        self._game_slots.extend(self.load_game_slots(slots, self.SLOTS_Y_VAL))

    def load_game_cards_for_hand(self, hand, y_val):
        game_cards = []
        x_val = 100
        for card in hand.cards:
            game_cards.append(self.load_game_card(card, x_val, y_val))
            x_val += 50
        return game_cards

    def load_game_card(self, card, x_val, y_val):
        pos = [x_val, y_val]
        gc = GameCard(card, pos, self.GAMECARD_SIZE)
        return gc

    def load_game_slots(self, slots, y_val):
        game_slots = []
        x_val = 50
        for slot in slots:
            game_slots.append(self.load_game_slot(slot, x_val, y_val))
            x_val += 50
        return game_slots

    def load_game_slot(self, slot, x_val, y_val):
        pos = [x_val, y_val]
        gs = GameSlot(slot, pos, self.GAMECARD_SIZE)
        return gs


class GameSlot:
    GAMECARD_SIZE = [40, 50]
    SLOT_COLOUR = (0, 0, 0)

    def __init__(self, slot, pos, size):
        self._slot = slot
        self._game_cards = []
        self._pos = pos
        self._size = size
        self._slot_surface = pygame.Surface(self._size)

        # Rect for collision detection
        x, y = self._pos
        w, h = self._size
        self._rect = pygame.Rect(x, y, w, h)

    @property
    def slot(self):
        return self._slot

    @property
    def rect(self):
        return self._rect

    @property
    def game_cards(self):
        return self._game_cards

    def render(self, surface):
        x, y = self._pos
        w, h = self._size
        pygame.draw.rect(self._slot_surface, self.SLOT_COLOUR, (0, 0, w, h))
        surface.blit(self._slot_surface, self._pos)
        for game_card in self.game_cards:
            game_card.render(surface)

    def handle_release(self, game_cards, clicked_card, hand, game_slots):
        self._game_cards.append(clicked_card)
        game_cards.remove(clicked_card)
        x, y = self._pos
        if hand.hand_no == 1:
            new_y = y + 50
            new_y += len(self._slot.p1_played) * 35
        else:
            new_y = y - 50
            new_y -= len(self._slot.p2_played) * 35
        clicked_card.move(x, new_y)
        self._slot.play_card(clicked_card.card, hand)
        slots = []
        for game_slot in game_slots:
            slots.append(game_slot.slot)
        self.check_and_handle_win(slots)

    def check_and_handle_win(self, slots):
        result = self._slot.check_winner(slots)
        if result == 1:
            self.SLOT_COLOUR = (244, 146, 162)
        elif result == 2:
            self.SLOT_COLOUR = (160, 244, 200)


class GameCard:
    def __init__(self, card, pos, size):
        self._card = card
        self._pos = pos
        self._size = size
        self._card_surface = pygame.Surface(self._size)

        # Rect for collision detection
        x, y = self._pos
        w, h = self._size
        self._rect = pygame.Rect(x, y, w, h)

        self._font = pygame.font.SysFont('Helvetica Neue', 40)

    @property
    def card(self):
        return self._card

    @property
    def rect(self):
        return self._rect

    def move(self, x, y):
        self.move_rect(x, y)
        self.pos = (x, y)

    # Move rect to specified x and y coordinates
    def move_rect(self, x, y):
        old_x = self._rect.x
        old_y = self._rect.y
        print("old rect pos: " + str(old_x) + "," + str(old_y))
        print("new pos: " + str(x) + "," + str(y))
        diff_x = x - old_x
        diff_y = y - old_y
        print("diff: " + str(diff_x) + "," + str(diff_y))
        self._rect.move_ip(diff_x, diff_y)
        print("new rect pos: " + str(self._rect.x) + "," + str(self._rect.y))
        print("rect size: " + str(self._rect.w) + "," + str(self._rect.h))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    def render(self, surface):
        val = self._card.val
        colour = self.get_colour(self._card)
        w, h = self._size
        pygame.draw.rect(self._card_surface, colour, (0, 0, w, h))
        self._card_surface.blit(self._font.render(str(val), True, (250, 250, 250)),
                                [5, 10])
        surface.blit(self._card_surface, self._pos)

    def get_colour(self, card):
        colour = card.colour
        if colour == Colour.RED:
            return 250, 100, 100
        elif colour == Colour.ORANGE:
            return 250, 150, 80
        elif colour == Colour.YELLOW:
            return 245, 250, 80
        elif colour == Colour.GREEN:
            return 100, 250, 100
        elif colour == Colour.BLUE:
            return 100, 100, 250
        elif colour == Colour.PURPLE:
            return 180, 100, 250


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
