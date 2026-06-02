from random import Random

from .card import Card


class Deck:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK: list[int] = []

    def __init__(self, seed: int = None) -> None:
        self._random = Random(seed)
        self.cards = Deck.GetFullDeck()
        self._random.shuffle(self.cards)

    @DeprecationWarning
    def shuffle(self) -> None:
        '''left in for compatibility'''
        # make new deck and then shuffle
        self.cards = Deck.GetFullDeck()
        self._random.shuffle(self.cards)
        

    def draw(self, n: int = 1) -> list[int]:
        cards = []
        for _ in range(n):
            cards.append(self.cards.pop())
        return cards
    
    def pull(self, card: int) -> int:
        self.cards.remove(card)
        return card
    
    def pull_many(self, cards: list[int]) -> list[int]:
        for card in cards:
            self.cards.remove(card)
        return cards

    def sorted_print(self) -> None:
        print(Card.ints_to_pretty_str(sorted(self.cards)))

    def __str__(self) -> str:
        return Card.ints_to_pretty_str(self.cards)

    @staticmethod
    def GetFullDeck() -> list[int]:
        if Deck._FULL_DECK:
            return list(Deck._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit in Card.STR_SUITS:
                Deck._FULL_DECK.append(Card.new(rank + suit))

        return list(Deck._FULL_DECK)