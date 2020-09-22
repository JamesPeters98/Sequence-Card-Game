import random
from typing import List

from Card import *
from Deck import Deck
from Player import Player

WIN_CONDITION = 5
COMPLETED_LINES = 2

ROWS = 10
COLS = 10


# Static methods
def is_player_spot(card: Card, player) -> bool:
    return card.selection == player or card.wildcard


class Game:

    def __init__(self):
        self.winner = 0
        self.draw = False
        self.has_winner = False
        self.table: List[List[Card]] = [
            [W_C.copy(), S_10.copy(), S_Q.copy(), S_K.copy(), S_A.copy(), D_2.copy(), D_3.copy(), D_4.copy(),
             D_5.copy(), W_C.copy()],
            [S_9.copy(), H_10.copy(), H_9.copy(), H_8.copy(), H_7.copy(), H_6.copy(), H_5.copy(), H_4.copy(),
             H_3.copy(), D_6.copy()],
            [S_8.copy(), H_Q.copy(), D_7.copy(), D_8.copy(), D_9.copy(), D_10.copy(), D_Q.copy(), D_K.copy(),
             H_2.copy(), D_7.copy()],
            [S_7.copy(), H_K.copy(), D_6.copy(), C_2.copy(), H_A.copy(), H_K.copy(), H_Q.copy(), D_A.copy(), S_2.copy(),
             D_8.copy()],
            [S_6.copy(), H_A.copy(), D_5.copy(), C_3.copy(), H_4.copy(), H_3.copy(), H_10.copy(), C_A.copy(),
             S_3.copy(), D_9.copy()],
            [S_5.copy(), C_2.copy(), D_4.copy(), C_4.copy(), H_5.copy(), H_2.copy(), H_9.copy(), C_K.copy(), S_4.copy(),
             D_10.copy()],
            [S_4.copy(), C_3.copy(), D_3.copy(), C_5.copy(), H_6.copy(), H_7.copy(), H_8.copy(), C_Q.copy(), S_5.copy(),
             D_Q.copy()],
            [S_3.copy(), C_4.copy(), D_2.copy(), C_6.copy(), C_7.copy(), C_8.copy(), C_9.copy(), C_10.copy(),
             C_6.copy(), D_K.copy()],
            [S_2.copy(), C_5.copy(), S_A.copy(), S_K.copy(), S_Q.copy(), S_10.copy(), S_9.copy(), S_8.copy(),
             S_7.copy(), D_A.copy()],
            [W_C.copy(), C_6.copy(), C_7.copy(), C_8.copy(), C_9.copy(), C_10.copy(), C_Q.copy(), C_K.copy(),
             C_A.copy(), W_C.copy()],
        ]

        self.deck = Deck()
        self.player1 = Player(self.deck, 1, self)
        self.player2 = Player(self.deck, 2, self)
        # self.player_turn = 1

    def init_game(self):
        print("New Game!")
        self.print_board()

    def is_valid_card_to_play(self, player_num: int, coord: (int, int)):
        player: Player = self.player1 if player_num == 1 else self.player2
        playable_coords = player.get_playable_coords(self)
        print(f'Playable coords: {playable_coords}')
        for playable_coord_tuple in playable_coords:
            for playable_coord in playable_coord_tuple:
                if coord == playable_coord:
                    return True

        return False

    def cards_to_string(self, cards: List[Card]):
        string: str = "Cards: "
        for card in cards:
            string = string + card.get_name() + ", "
        return string

    def do_ai_turn(self, player_num: int):
        player: Player = self.player1 if player_num == 1 else self.player2
        print(f'AI player: {player.player_num}')

        cards: List[Card] = player.get_playable_cards(self.table)
        random.shuffle(cards)
        print(f'AI playable cards: {self.cards_to_string(cards)}')
        card: Card = cards[0]

        # Crashes because JACK doesn't give coords
        coords = player.get_card_coords(card, self)
        random.shuffle(coords)
        print(f'AI coords: {coords}')
        coord = coords[0]

        print(f'AI playing card: {card.get_name()}')
        self.do_turn(player_num, card, coord)

    # card is the card from the players
    def do_turn(self, player_num: int, card: Card, coord):

        # Calculate who the current player is
        player: Player = self.player1 if player_num == 1 else self.player2

        if self.has_winner:
            print("Game has winner")
        if len(self.deck.cards) == 0:
            self.draw = True
            print("Game ended in draw!")
            return

        # cards: List[Card] = player.get_playable_cards(self.table)
        # random.shuffle(cards)
        # card: Card = cards[0]
        print(f'Player {player_num}\'s turn')
        sel_card = self.table[coord[0]][coord[1]]
        print(f'Selecting card: {sel_card.get_name()}')

        print(f'Playing card: {card.get_name()}')
        if card.rank != Rank.JACK:
            # coords = player.get_card_coords(card, self.table)
            # random.shuffle(coords)
            # coord = coords[0]
            # print(f'Possible coords: {coords}')
            print(f'Coord selected: {coord}')
            # plays the card
            self.table[coord[0]][coord[1]].selection = player.player_num
        # Two eyed jack can place anywhere
        elif card.suit == Suit.CLUB or card.suit == Suit.DIAMOND:
            # free_spots = self.get_free_spots(0)
            # # The AI should select the best spot based on these values
            # random.shuffle(free_spots)
            self.table[coord[0]][coord[1]].selection = player.player_num
        # One eyed jack can remove other players tokens
        else:
            # opponent_spots = self.get_free_spots(opponent.player_num)
            # random.shuffle(opponent_spots)
            # self.table[opponent_spots[0][0]][opponent_spots[0][1]].selection = 0
            self.table[coord[0]][coord[1]].selection = 0

        if self.check_for_completed_line(player.player_num):
            player.completed_lines += 1
            print(f'Player {player.player_num} has completed a line!')
            if player.completed_lines >= COMPLETED_LINES:
                self.has_winner = True
                self.winner = player.player_num
                print(f'Player {player.player_num} has won!')

        # Remove card from players hand and draw new card
        player.play_card(card)
        self.print_board()

    # Returns all the free spots on the board
    def get_free_spots(self, selection: int):
        free_spots = []
        for row in range(0, ROWS):
            for col in range(0, COLS):
                # print(f'Checking free spot in ({row},{col})')
                card: Card = self.table[row][col]
                if card.selection == selection and not card.is_complete:
                    free_spots.append((row, col))

        return free_spots

    # Checks for a new completed line for the player
    # Result can be used to count the number of completed lines for the player
    def check_for_completed_line(self, player: int) -> bool:
        # Horizontal check
        # print("Doing horizontal check")
        for col in range(0, COLS + 1 - WIN_CONDITION):
            for row in range(0, ROWS):
                # print(f'Checking horizontal check at pos ({row},{col})')
                if self.check_line(row, col, 0, 1, player):
                    return True

        # print("Doing vertical check")
        # Vertical check
        for row in range(0, ROWS + 1 - WIN_CONDITION):
            for col in range(0, COLS):
                if self.check_line(row, col, 1, 0, player):
                    return True

        # print("Diagonal up check")
        # Diagonal up
        for row in range(WIN_CONDITION - 1, ROWS):
            for col in range(0, COLS - WIN_CONDITION + 1):
                if self.check_line(row, col, -1, 1, player):
                    return True

        # print("Diagonal down check")
        # Diagonal down
        for row in range(WIN_CONDITION - 1, ROWS):
            for col in range(WIN_CONDITION - 1, COLS):
                if self.check_line(row, col, -1, -1, player):
                    return True

        return False

    # start_row must be less than the max self.table row by WIN_CONDITION same for start_col
    def check_line(self, start_row: int, start_col: int, row_direction, col_direction, player) -> bool:
        # Can only have 1 completed card part of a new completed line.
        completed_cards: int = 0
        # print(f'start coordinates ({start_row}, {start_col}) ')
        for i in range(0, WIN_CONDITION):
            row = start_row + i * row_direction
            col = start_col + i * col_direction

            # print(f'Checking coordinates ({row}, {col}) ')
            card: Card = self.table[row][col]
            # Only one completed card is allowed in a new line (Lines can cross over each other)
            if card.is_complete:
                completed_cards += 1
                if completed_cards > 1:
                    return False

            if not is_player_spot(card, player):
                return False

        for i in range(0, WIN_CONDITION):
            row = start_row + i * row_direction
            col = start_col + i * col_direction
            card: Card = self.table[row][col]
            if not card.wildcard:
                card.is_complete = True

        # Line has 5 in a row
        return True

    def print_board(self):
        print('---------------------------------------')
        print('\n'.join([''.join(['{:4}'.format(item.to_string()) for item in row])
                         for row in self.table]))
        print('---------------------------------------')
