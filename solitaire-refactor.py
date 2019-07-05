#!/bin/env python3

# Thanks to Fluent Python by Luciano Ramalho for the start of the Deck class

from random import shuffle

class Card:
    def __init__(self, rank='', suit='', visible=True):
        self.rank=rank
        self.suit=suit
        self.visible=visible

    def __repr__(self):
        if self.visible:
            return 'Card(%s, %s)' % (self.rank, self.suit)
        else:
            return 'Card(None, None)'
    def __str__(self):
        if self.visible:
            return '%s of %s' % (self.rank, self.suit)
        else:
            return 'Upside-down card'

    def flip(self):
        self.visible = not self.visible
        

class Deck:
    ranks = list('A')+[str(rank) for rank in range(2,11)]+list('JQK')
    suits = 'Spades Hearts Diamonds Clubs'.split()

    def __init__(self, starting_cards=False):
        if isinstance(starting_cards, list) and \
            all(isinstance(card, Card)
            for card in starting_cards):
            #If we are given a list of cards, use that
            self._cards=starting_cards
        else:
            #Otherwise make a standard deck
            self._cards=[Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self._cards) 

    def __getitem__(self, position):
        return self._cards[position]

    def shuffle(self):
        shuffle(self._cards)
        return

    #this can be super cleaned up with 'in' and slices
    def can_stack(self, top_card, base_card):
        if ((base_card.suit == self.suits[0] or
             base_card.suit == self.suits[3]) and 
            (top_card.suit == self.suits[1] or
             top_card.suit == self.suits[2])) or \
           ((base_card.suit == self.suits[1] or
             base_card.suit == self.suits[2]) and 
            (top_card.suit == self.suits[0] or
             top_card.suit == self.suits[3])):
            #If black on red or red on black
            if self.ranks.index(top_card.rank) \
                - self.ranks.index(base_card.rank) == -1:
                #And the new card is one lower than the old
                return True
        else:
            return False

def deal(from_deck, to_deck, count):
    try:
        new_to_deck=Deck([card for card in reversed(from_deck[:count])] + to_deck[:])
        new_from_deck=Deck(from_deck[count:])
    except:
        print("Oops, couldn't deal")
    return (new_from_deck, new_to_deck)

def move_stack(from_deck, to_deck, count):
    try:
        new_to_deck=Deck(from_deck[:count] + to_deck[:])
        new_from_deck=Deck(from_deck[count:])
    except:
        print("Oops, couldn't move stack")
    return (new_from_deck, new_to_deck)


def flip_deck(deck):
    for card in deck:
        card.flip()

class Solitaire:
    menu_instructions = ("Action Menu\n"
                         "---------------\n"
                         "- 'm [source] [dest]' to move from one tableau stack to another\n"
                         "- 'b [source]' to move from a stack to the foundations, [source] t for talon\n"
                         "- 'p'[dest] to move from the talon to a tableau stack\n"
                         "- 'f' to flip another card over from the stock\n"
                         "- 'q' to quit\n"
                        )

    def __init__(self):
        #set up card piles
        self.piles = {
                        ('foundation', x)   :   Deck([])    for x in range(4),
                        ('tableau', x)      :   Deck([])    for x in range(7),
                        'talon'             :   Deck([]),
                        'stock'             :   Deck()      #all cards start here
                     }
        #self.foundations=[Deck([]) for x in range(4)]
        #self.tableau=[Deck([]) for x in range(7)]
        #self.talon=Deck([])
        #self.stock=Deck()

        #prep cards
        self.piles['stock'].shuffle()
        for x in range(7):
            self.stock, self.tableau[x] = deal(self.stock, self.tableau[x], x)
            flip_deck(self.tableau[x])
            self.stock, self.tableau[x] = deal(self.stock, self.tableau[x], 1)
        flip_deck(self.stock)

    def __str__(self):
        desc = ''

        desc += 'Foundations\n'
        for pile in game.foundations:
            desc += pile.suits[game.foundations.index(pile)] + ' foundation.\n'
            for card in pile:
                desc += '%s\n' % card
            desc += '\n'
        desc += '\n'

        desc += 'Stock\n'
        for card in game.stock:
            desc += '%s\n' % card

        desc += '\nTalon\n'
        for card in game.talon:
            desc += '%s\n' % card

        desc += '\n'
        index = 0
        for pile in game.tableau:
            index += 1
            desc += 'Tableau Pile %i\n' % index
            for card in pile:
                desc += '%s\n' % card
            desc += '\n'
        return desc

    def put_to_play(self, to_index):
        #validate
        card = self.talon[0]
        #print("Does %s go on top of %s" % (card, self.tableau[to_index][0]))
        can_stack = False
        if len(self.tableau[to_index]) == 0:
            if card.rank == 'K':
                can_stack = True
                print("it's a king")
        elif self.tableau[to_index].can_stack(card, self.tableau[to_index][0]):
            can_stack = True
        
        if can_stack:
            #print('Yes it can')
            self.talon, self.tableau[to_index] = move_stack(
                    self.talon,
                    self.tableau[to_index],
                    1)
        #else:
            #print("No it can't")
        
        return


    def transfer(self, from_index, to_index):
        #validate
        transfer_depth = 0
        for card in self.tableau[from_index]:
            transfer_depth += 1
            if transfer_depth > len(self.tableau[from_index]):
                break
            if card.visible:
                #print("Does %s go on top of %s?" % (card, self.tableau[to_index][0]))
                can_stack = False
                if len(self.tableau[to_index]) == 0:
                    if card.rank == 'K':
                        can_stack = True
                elif self.tableau[from_index].can_stack(card, self.tableau[to_index][0]):
                    can_stack = True
                if can_stack:
                    #print('Yes it can')
                    break
                #else:
                    #print("No it can't")
            else:
                #print("End of visible cards reached.")
                transfer_depth = 0
                break
        
        if transfer_depth:
            self.tableau[from_index], self.tableau[to_index] = move_stack(
                self.tableau[from_index],
                self.tableau[to_index],
                transfer_depth)
        return

    #very ugly copy paste
    def build(self, source_index):
        if source_index == -1:
            card = self.talon[0]
            suit_index = self.talon.suits.index(card.suit)
            foundation_height = -1
            if len(self.foundations[suit_index]) > 0:
                foundation_height = self.talon.ranks.index(self.foundations[suit_index][0].rank) 
            if self.talon.ranks.index(card.rank) - foundation_height == 1:
                self.talon = Deck(self.talon[1:])
                self.foundations[suit_index] = Deck([card] + self.foundations[suit_index][:])
                return True
            return False
        else:
            card = self.tableau[source_index][0]
            suit_index = self.tableau[source_index].suits.index(card.suit)
            foundation_height = -1
            if len(self.foundations[suit_index]) > 0:
                foundation_height = self.tableau[source_index].ranks.index(self.foundations[suit_index][0].rank) 
            if self.tableau[source_index].ranks.index(card.rank) - foundation_height == 1:
                self.tableau[source_index] = Deck(self.tableau[source_index][1:])
                self.foundations[suit_index] = Deck([card] + self.foundations[suit_index][:])
                return True
            return False

    def flip_stock(self):
        if len(self.stock) == 0:
            self.talon, self.stock = deal(self.talon, self.stock, len(self.talon))
            flip_deck(self.stock)
        
        flip_deck(self.stock)
        self.stock, self.talon = deal(self.stock, self.talon, 1)
        flip_deck(self.stock)
        return

    def check_tableau(self):
        for x in range(7):
            if len(self.tableau[x]) > 0 and not self.tableau[x][0].visible:
                self.tableau[x][0].flip()



def game_loop(game):
    #Show game
    print(game)

    #game loop
    while True:
        print(game.menu_instructions)
        #Prompt for decision
        decision = input('> ').split()
        #for word in decision:
        #    print(word)
        #Validate input
        if len(decision) > 0:
            if decision[0] == 'm':
                game.transfer(int(decision[1])-1, int(decision[2])-1)
                game.check_tableau()
            elif decision[0] == 'b':
                if decision[1] == 't':
                    game.build(-1)
                else:
                    game.build(int(decision[1])-1)
                    game.check_tableau()
            elif decision[0] == 'p':
                game.put_to_play(int(decision[1])-1)
            elif decision[0] == 'f':
                game.flip_stock()
            elif decision[0] == 'q':
                break
        #Perform action
        #Check for victory
        #Show game
        print(game)
        
    return

game = Solitaire()
game_loop(game)

#print(game)
#
#for x in range(3):
#    game.flip_stock()
#
#print(game)
#
#game.transfer(1, 2)
#game.check_tableau()
#
#print(game)
#
#for i in range(7):
#    if game.build(i):
#        print("successfully moved index %i to foundation" % (i+1))
#    else:
#        print("couldn't move index %i to foundation" % (i+1))
#
#game.check_tableau()
#game.put_to_play(3)

#print(game)



