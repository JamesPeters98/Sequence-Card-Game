import os
from typing import List

from Game import Game, Card
import pygame
import pygbutton
from pygame import gfxdraw

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

PLAYER_1_COLOR = GREEN
PLAYER_2_COLOR = BLUE


class Gui:
    gameDisplay = None

    def __init__(self, game: Game):
        self.display_cards: List[DisplayCard] = []
        self.player_hand: List[HandCard] = []
        pygame.init()
        Gui.gameDisplay = pygame.display.set_mode((1280, 900))
        pygame.display.set_caption("Sequence Card Game")
        clock = pygame.time.Clock()

        self.hand_list = pygame.sprite.Group()

        self.init_display_cards(game)
        self.update_player_hand(game)

        self.card_list = pygame.sprite.Group()
        self.chip_list = pygame.sprite.Group()

        for card in self.display_cards:
            self.card_list.add(card)

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        width = Gui.gameDisplay.get_size()[0]
        height = Gui.gameDisplay.get_size()[1]
        self.button = pygbutton.PygButton((width - 150, height - 50, 100, 30), "Simulate Turn")

        self.player_won_text = None
        self.player_won_rect = None

        running = True

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if 'click' in self.button.handleEvent(event):
                    game.do_ai_turn(1)
                    if not game.has_winner:
                        game.do_ai_turn(2)
                    self.do_turn_update(game)

                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = event.pos

                    for card in self.display_cards:
                        if card.rect.collidepoint(mouse):
                            print(f'Card clicked: {card.card.get_name()}')
                            pos = (card.row, card.col)
                            if game.is_valid_card_to_play(1, pos):
                                card_from_hand = game.player1.get_card_from_hand(pos, game)
                                print(f'Playing card from hand {card_from_hand.get_name()}')
                                game.do_turn(1, card_from_hand, pos)

                                if not game.has_winner:
                                    game.do_ai_turn(2)

                                self.do_turn_update(game)
                            else:
                                print("That card isn't valid to play")

                    for card in self.player_hand:
                        if card.rect.collidepoint(mouse):
                            print(f'Player hand card clicked: {card.card.get_name()}')
                            match_card = game.player1.find_matching_card(card.card)
                            playable_coords = game.player1.get_card_coords(match_card, game)
                            print(f'Playable coords: {playable_coords}')

            Gui.gameDisplay.fill(BLACK)

            self.card_list.draw(Gui.gameDisplay)
            self.hand_list.draw(Gui.gameDisplay)

            for card in self.display_cards:
                # self.chip_list = pygame.sprite.Group()
                if card.chip.is_enabled:
                    card.chip.draw()
                    # self.chip_list.add(card.chip)

            self.chip_list.draw(Gui.gameDisplay)
            self.button.draw(Gui.gameDisplay)

            if game.has_winner:
                Gui.gameDisplay.blit(self.player_won_text, self.player_won_rect)

            pygame.display.update()
            clock.tick(60)

    def do_turn_update(self, game: Game):
        if game.has_winner:
            self.player_won_text = self.font.render(f'Player {game.winner} has won!', True, WHITE)
            self.player_won_rect = self.player_won_text.get_rect()
            self.player_won_rect.center = (Gui.gameDisplay.get_size()[0] / 2, Gui.gameDisplay.get_size()[1] - 25)

        self.update_display_cards(game)
        self.update_player_hand(game)

    def init_display_cards(self, game: Game):
        row_num = 0
        for row in game.table:
            col_num = 0
            for card in row:
                self.display_cards.append(DisplayCard(card, row_num, col_num))
                col_num += 1
            row_num += 1

    def update_player_hand(self, game: Game):
        index = 0
        self.player_hand = []
        for card in game.player1.hand:
            self.player_hand.append(HandCard(card, index))
            index += 1

        self.hand_list = pygame.sprite.Group()
        for card in self.player_hand:
            self.hand_list.add(card)

    def update_display_cards(self, game: Game):
        for card in self.display_cards:
            card.update(game)


class DisplayCard(pygame.sprite.Sprite):
    CARD_X_START = 140
    CARD_Y_START = 30
    CARD_FACTOR = 0.125
    X_PADDING = 8
    Y_PADDING = 4

    def __init__(self, card: Card, row, col):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", "cards", f'{card.to_filename()}.png'))
        self.card = card
        self.row = row
        self.col = col

        self.size = self.image.get_size()
        self.CARD_WIDTH = int(self.size[0] * DisplayCard.CARD_FACTOR)
        self.CARD_HEIGHT = int(self.size[1] * DisplayCard.CARD_FACTOR)

        self.image = pygame.transform.smoothscale(self.image, (self.CARD_WIDTH, self.CARD_HEIGHT))
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.set_pos(col, row)

        self.chip: Chip = Chip(*self.get_center())

    def set_pos(self, x: int, y: int):
        self.rect.x = DisplayCard.CARD_X_START + x * (self.CARD_HEIGHT + DisplayCard.X_PADDING)
        self.rect.y = DisplayCard.CARD_Y_START + y * (self.CARD_WIDTH + DisplayCard.Y_PADDING)

    def get_center(self) -> (int, int):
        return self.rect.x + self.CARD_HEIGHT / 2, self.rect.y + self.CARD_WIDTH / 2

    def update(self, game: Game):
        card = game.table[self.row][self.col]
        self.chip.is_enabled = card.selection != 0
        self.chip.is_complete = card.is_complete

        if card.selection == 1:
            self.chip.color = PLAYER_1_COLOR
        if card.selection == 2:
            self.chip.color = PLAYER_2_COLOR


class HandCard(pygame.sprite.Sprite):
    CARD_X_START = 255
    CARD_FACTOR = 0.2
    X_PADDING = 8

    def __init__(self, card: Card, index: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", "cards", f'{card.to_filename()}.png'))
        self.card = card

        self.size = self.image.get_size()
        self.CARD_WIDTH = int(self.size[0] * HandCard.CARD_FACTOR)
        self.CARD_HEIGHT = int(self.size[1] * HandCard.CARD_FACTOR)

        self.image = pygame.transform.smoothscale(self.image, (self.CARD_WIDTH, self.CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.y = Gui.gameDisplay.get_size()[1] - 200

        self.set_pos(index)

    def set_pos(self, x: int):
        self.rect.x = HandCard.CARD_X_START + x * (self.CARD_WIDTH + HandCard.X_PADDING)


class Chip:

    def __init__(self, center_x: int, center_y: int):
        self.center_x = center_x
        self.center_y = center_y
        self.is_enabled = False
        self.color = (0, 0, 0)
        self.is_complete = False

        # self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # pygame.draw.circle(self.image, red, (int(self.center_x), int(self.center_y)), 10)
        # # pygame.gfxdraw.filled_circle(self.image, 15, 15, 14, (0, 255, 0))
        # self.rect = self.image.get_rect()

    def draw(self):
        pygame.gfxdraw.aacircle(Gui.gameDisplay, int(self.center_x), int(self.center_y), 15, self.color)
        pygame.gfxdraw.filled_circle(Gui.gameDisplay, int(self.center_x), int(self.center_y), 15, self.color)
        if self.is_complete:
            pygame.gfxdraw.aacircle(Gui.gameDisplay, int(self.center_x), int(self.center_y), 5, WHITE)
            pygame.gfxdraw.filled_circle(Gui.gameDisplay, int(self.center_x), int(self.center_y), 5, WHITE)
