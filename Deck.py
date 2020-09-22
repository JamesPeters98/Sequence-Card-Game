from typing import List, Optional

from Card import Card, Suit, Rank
import random


class Deck(object):
    cards: List[Card] = []

    def __init__(self):
        # Add two of every card to the deck and then shuffle
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
                self.cards.append(Card(suit, rank))

        random.shuffle(self.cards)

    def next_card(self) -> Optional[Card]:
        if len(self.cards) == 0:
            return None
        card = self.cards[0]
        self.cards.pop(0)
        print(f'Drew a card, cards remaining: {len(self.cards)}')
        return card
