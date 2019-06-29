#!/bin/env python3

# Thanks to Fluent Python by Luciano Ramalho for the start of the Deck class

from random import shuffle

class Card:
    def __init__(self, rank='', suit=''):
        self.rank=rank
        self.suit=suit

    def __repr__(self):
        return 'Card(%s, %s)' % (self.rank, self.suit)

class Deck:
    ranks = [str(rank) for rank in range(2,11)]+list('JQKA')
    suits = 'spades hearts diamonds clubs'.split()

    def __init__(self, starting_cards=False):
        if isinstance(starting_cards, list) and all(isinstance(card, Card) for card in starting_cards):
            self._cards=cards
        else:
            self._cards=[Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards) 

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        shuffle(self._cards)
        return

my_deck1=Deck()
my_deck2=Deck(my_deck1[:14])
my_deck2.shuffle()
for card in my_deck2:
    print(card)
