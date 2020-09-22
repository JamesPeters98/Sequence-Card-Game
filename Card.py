import copy
import enum


class Suit(enum.Enum):
    HEART = 0
    DIAMOND = 1
    SPADE = 2
    CLUB = 3


class Rank(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Card(object):
    selection: int = 0
    # True when this card is part of a complete set.
    is_complete: bool = False
    rank: Rank
    suit: Suit

    def __init__(self, suit, rank, wildcard=False):
        self.rank = rank
        self.suit = suit
        self.wildcard = wildcard

        # if wildcard:
        #     print(f'Created a wildcard')
        # else:
        #     print(f'Created a {rank.name} of {suit.name}')

    def get_name(self):
        if self.wildcard:
            return "Wildcard"
        return f'{self.rank.name} of {self.suit.name}'

    def copy(self):
        return copy.copy(self)

    def match(self, card):
        return (card.suit == self.suit) and (card.rank == self.rank)

    def to_string(self):
        val: str = 'x' if self.wildcard else self.selection
        if self.is_complete:
            return f'[{val}]'
        else:
            return f' {val} '

    def to_filename(self):
        return f'{from_rank(self.rank)}{from_suit(self.suit)}'


def from_rank(rank: Rank) -> str:
    switcher = {
        Rank.KING: "K",
        Rank.QUEEN: "Q",
        Rank.JACK: "J",
        Rank.ACE: "A",
        # Wildcards have rank as 0 so return the back of a card as the result
        0: "black_joker"
    }
    val = switcher.get(rank, str(rank.value) if isinstance(rank, Rank) else rank)
    return val


def from_suit(suit: Suit):
    switcher = {
        Suit.CLUB: "C",
        Suit.SPADE: "S",
        Suit.HEART: "H",
        Suit.DIAMOND: "D",
        0: ""
    }
    val = switcher.get(suit)
    return val


# Wildcard
W_C = Card(0, 0, wildcard=True)

# Spades
S_A = Card(Suit.SPADE, Rank.ACE)
S_2 = Card(Suit.SPADE, Rank.TWO)
S_3 = Card(Suit.SPADE, Rank.THREE)
S_4 = Card(Suit.SPADE, Rank.FOUR)
S_5 = Card(Suit.SPADE, Rank.FIVE)
S_6 = Card(Suit.SPADE, Rank.SIX)
S_7 = Card(Suit.SPADE, Rank.SEVEN)
S_8 = Card(Suit.SPADE, Rank.EIGHT)
S_9 = Card(Suit.SPADE, Rank.NINE)
S_10 = Card(Suit.SPADE, Rank.TEN)
S_J = Card(Suit.SPADE, Rank.JACK)
S_Q = Card(Suit.SPADE, Rank.QUEEN)
S_K = Card(Suit.SPADE, Rank.KING)

# Clubs
C_A = Card(Suit.CLUB, Rank.ACE)
C_2 = Card(Suit.CLUB, Rank.TWO)
C_3 = Card(Suit.CLUB, Rank.THREE)
C_4 = Card(Suit.CLUB, Rank.FOUR)
C_5 = Card(Suit.CLUB, Rank.FIVE)
C_6 = Card(Suit.CLUB, Rank.SIX)
C_7 = Card(Suit.CLUB, Rank.SEVEN)
C_8 = Card(Suit.CLUB, Rank.EIGHT)
C_9 = Card(Suit.CLUB, Rank.NINE)
C_10 = Card(Suit.CLUB, Rank.TEN)
C_J = Card(Suit.CLUB, Rank.JACK)
C_Q = Card(Suit.CLUB, Rank.QUEEN)
C_K = Card(Suit.CLUB, Rank.KING)

# Diamonds
D_A = Card(Suit.DIAMOND, Rank.ACE)
D_2 = Card(Suit.DIAMOND, Rank.TWO)
D_3 = Card(Suit.DIAMOND, Rank.THREE)
D_4 = Card(Suit.DIAMOND, Rank.FOUR)
D_5 = Card(Suit.DIAMOND, Rank.FIVE)
D_6 = Card(Suit.DIAMOND, Rank.SIX)
D_7 = Card(Suit.DIAMOND, Rank.SEVEN)
D_8 = Card(Suit.DIAMOND, Rank.EIGHT)
D_9 = Card(Suit.DIAMOND, Rank.NINE)
D_10 = Card(Suit.DIAMOND, Rank.TEN)
D_J = Card(Suit.DIAMOND, Rank.JACK)
D_Q = Card(Suit.DIAMOND, Rank.QUEEN)
D_K = Card(Suit.DIAMOND, Rank.KING)

# Hearts
H_A = Card(Suit.HEART, Rank.ACE)
H_2 = Card(Suit.HEART, Rank.TWO)
H_3 = Card(Suit.HEART, Rank.THREE)
H_4 = Card(Suit.HEART, Rank.FOUR)
H_5 = Card(Suit.HEART, Rank.FIVE)
H_6 = Card(Suit.HEART, Rank.SIX)
H_7 = Card(Suit.HEART, Rank.SEVEN)
H_8 = Card(Suit.HEART, Rank.EIGHT)
H_9 = Card(Suit.HEART, Rank.NINE)
H_10 = Card(Suit.HEART, Rank.TEN)
H_J = Card(Suit.HEART, Rank.JACK)
H_Q = Card(Suit.HEART, Rank.QUEEN)
H_K = Card(Suit.HEART, Rank.KING)
