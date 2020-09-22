from typing import List, Optional

import Game
from Card import Card, Rank, Suit
from Deck import Deck


class Player:

    def __init__(self, deck: Deck, player_num: int, game: Game):
        self.player_num = player_num
        self.hand: List[Card] = []
        self.deck = deck
        self.completed_lines = 0
        self.game = game

        for i in range(0, 7):
            self.hand.append(deck.next_card())

        print(f'Player {player_num} has cards: {self.cards_in_hand()}')

    def cards_in_hand(self) -> str:
        string: str = "Hand: "
        for card in self.hand:
            string = string + card.get_name() + ", "
        return string

    def get_playable_cards(self, table: List[List[Card]]) -> List[Card]:
        playable_cards: List[Card] = []

        for hand_card in self.hand:
            # print(f"Checking card: {hand_card.get_name()}")
            if hand_card.rank == Rank.JACK:
                if hand_card.suit == Suit.CLUB or hand_card.suit == Suit.DIAMOND:
                    playable_cards.append(hand_card) if hand_card not in playable_cards else playable_cards
                elif len(self.game.get_free_spots(self.get_opponent())) > 0:
                    playable_cards.append(hand_card) if hand_card not in playable_cards else playable_cards
            for row in table:
                for card in row:
                    if card.match(hand_card) and card.selection == 0:
                        playable_cards.append(hand_card) if hand_card not in playable_cards else playable_cards
                        break

        return playable_cards

    # Returns a card that can be played for the given coords
    def get_card_from_hand(self, coords: (int, int), game: Game):
        for hand_card in self.hand:
            card_coords = self.get_card_coords(hand_card, game)
            if coords in card_coords:
                return hand_card

    # Returns a list of tuples
    def get_card_coords(self, card: Card, game: Game) -> [()]:
        if card.rank == Rank.JACK:
            # Two eyed Jack can place anywhere
            if card.suit == Suit.CLUB or card.suit == Suit.DIAMOND:
                return game.get_free_spots(0)
            # One eyed Jack can only remove opponents counters
            else:
                return game.get_free_spots(self.get_opponent())

        coords_tuple = []

        # Adds the two cards from the board if available
        for row in range(0, len(game.table)):
            for col in range(0, len(game.table[row])):
                board_card = game.table[row][col]
                if board_card.match(card) and board_card.selection == 0:
                    coords_tuple.append((row, col))

        return coords_tuple

    def get_playable_coords(self, game: Game):
        coords = []
        playable_cards = self.get_playable_cards(game.table)

        for card in playable_cards:
            coords.append(self.get_card_coords(card, game))

        # print(f'Playable cards: {list(playable_cards)}')

        return coords

    def play_card(self, card: Card):
        print(f'Cards in hand: {self.cards_in_hand()}')
        card_to_play: Optional[Card] = self.find_matching_card(card)

        if card_to_play is None:
            raise Exception(f'Couldn\'t find card {card.get_name()} in hand')

        self.hand.remove(card_to_play)

        next_card: Optional[Card] = self.deck.next_card()
        if next_card is not None:
            self.hand.append(next_card)

    def get_opponent(self):
        return 2 if self.player_num == 1 else 1

    def find_matching_card(self, card: Card) -> Optional[Card]:
        for hand_card in self.hand:
            if hand_card.match(card):
                return hand_card

        # No matching card
        return None
