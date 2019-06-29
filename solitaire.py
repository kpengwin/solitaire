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
            self._cards=starting_cards
        else:
            self._cards=[Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards) 

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        shuffle(self._cards)
        return

def deal(from_deck, to_deck, count):
    try:
        new_to_deck=Deck([card for card in reversed(from_deck[:count])] + to_deck[:])
        new_from_deck=Deck(from_deck[count:])
    except:
        print("Oops, couldn't deal")
    return (new_from_deck, new_to_deck)


class Solitaire:
    
    def __init__(self):
        #set up card piles
        self.foundations=[Deck([]) for x in range(4)]
        self.tableau=[Deck([]) for x in range(7)]
        self.talon=Deck([])
        self.stock=Deck()

        #prep cards
        self.stock.shuffle()
        for x in range(7):
            self.stock, self.tableau[x] = deal(self.stock, self.tableau[x], x+1)

    def __str__(self):
        desc = "" 
        desc += "Stock\n"
        for card in game.stock:
            desc += "%s\n" % card

        desc += "\n"
        index = 0
        for pile in game.tableau:
            index += 1
            desc += "Tableau Pile %i\n" % index
            for card in pile:
                desc += "%s\n" % card
            desc += "\n"
        return desc

       

game = Solitaire()
print(game)

