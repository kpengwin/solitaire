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
    #def can_stack(self, top_card, base_card):
    #    if ((base_card.suit == self.suits[0] or
    #         base_card.suit == self.suits[3]) and 
    #        (top_card.suit == self.suits[1] or
    #         top_card.suit == self.suits[2])) or \
    #       ((base_card.suit == self.suits[1] or
    #         base_card.suit == self.suits[2]) and 
    #        (top_card.suit == self.suits[0] or
    #         top_card.suit == self.suits[3])):
    #        #If black on red or red on black
    #        if self.ranks.index(top_card.rank) \
    #            - self.ranks.index(base_card.rank) == -1:
    #            #And the new card is one lower than the old
    #            return True
    #    else:
    #        return False

#def deal(from_deck, to_deck, count):
#    try:
#        new_to_deck=Deck([card for card in reversed(from_deck[:count])] + to_deck[:])
#        new_from_deck=Deck(from_deck[count:])
#    except:
#        print("Oops, couldn't deal")
#    return (new_from_deck, new_to_deck)
#
#def move_stack(from_deck, to_deck, count):
#    try:
#        new_to_deck=Deck(from_deck[:count] + to_deck[:])
#        new_from_deck=Deck(from_deck[count:])
#    except:
#        print("Oops, couldn't move stack")
#    return (new_from_deck, new_to_deck)


#def flip_deck(deck):
#    for card in deck:
#        card.flip()

class Solitaire:
#    menu_instructions = ("Action Menu\n"
#                         "---------------\n"
#                         "- 'm [source] [dest]' to move from one tableau stack to another\n"
#                         "- 'b [source]' to move from a stack to the foundations, [source] t for talon\n"
#                         "- 'p'[dest] to move from the talon to a tableau stack\n"
#                         "- 'f' to flip another card over from the stock\n"
#                         "- 'q' to quit\n"
#                        )

    def __init__(self):
        #set up card piles
        self.piles = {
                        ('foundation', x)   :   Deck([])    for x in range(4),
                        ('tableau', x)      :   Deck([])    for x in range(7),
                        'talon'             :   Deck([]),
                        'stock'             :   Deck()      #all cards start here
                     }

        #grab a local copy of these for simplicity
        self.suits = self.piles['stock'].piles
        self.ranks = self.piles['stock'].rank
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

#    def put_to_play(self, to_index):
#        #validate
#        card = self.talon[0]
#        #print("Does %s go on top of %s" % (card, self.tableau[to_index][0]))
#        can_stack = False
#        if len(self.tableau[to_index]) == 0:
#            if card.rank == 'K':
#                can_stack = True
#                print("it's a king")
#        elif self.tableau[to_index].can_stack(card, self.tableau[to_index][0]):
#            can_stack = True
#        
#        if can_stack:
#            #print('Yes it can')
#            self.talon, self.tableau[to_index] = move_stack(
#                    self.talon,
#                    self.tableau[to_index],
#                    1)
#        #else:
#            #print("No it can't")
#        
#        return


#    def transfer(self, from_index, to_index):
#        #validate
#        transfer_depth = 0
#        for card in self.tableau[from_index]:
#            transfer_depth += 1
#            if transfer_depth > len(self.tableau[from_index]):
#                break
#            if card.visible:
#                #print("Does %s go on top of %s?" % (card, self.tableau[to_index][0]))
#                can_stack = False
#                if len(self.tableau[to_index]) == 0:
#                    if card.rank == 'K':
#                        can_stack = True
#                elif self.tableau[from_index].can_stack(card, self.tableau[to_index][0]):
#                    can_stack = True
#                if can_stack:
#                    #print('Yes it can')
#                    break
#                #else:
#                    #print("No it can't")
#            else:
#                #print("End of visible cards reached.")
#                transfer_depth = 0
#                break
#        
#        if transfer_depth:
#            self.tableau[from_index], self.tableau[to_index] = move_stack(
#                self.tableau[from_index],
#                self.tableau[to_index],
#                transfer_depth)
#        return
#
#    #very ugly copy paste
#    def build(self, source_index):
#        if source_index == -1:
#            card = self.talon[0]
#            suit_index = self.talon.suits.index(card.suit)
#            foundation_height = -1
#            if len(self.foundations[suit_index]) > 0:
#                foundation_height = self.talon.ranks.index(self.foundations[suit_index][0].rank) 
#            if self.talon.ranks.index(card.rank) - foundation_height == 1:
#                self.talon = Deck(self.talon[1:])
#                self.foundations[suit_index] = Deck([card] + self.foundations[suit_index][:])
#                return True
#            return False
#        else:
#            card = self.tableau[source_index][0]
#            suit_index = self.tableau[source_index].suits.index(card.suit)
#            foundation_height = -1
#            if len(self.foundations[suit_index]) > 0:
#                foundation_height = self.tableau[source_index].ranks.index(self.foundations[suit_index][0].rank) 
#            if self.tableau[source_index].ranks.index(card.rank) - foundation_height == 1:
#                self.tableau[source_index] = Deck(self.tableau[source_index][1:])
#                self.foundations[suit_index] = Deck([card] + self.foundations[suit_index][:])
#                return True
#            return False

    def _flip_deck(self, deck_key):
        assert deck_key in self.piles.keys(), "Can't flip, invalid pile."
        for card in self.piles[deck_key]:
            card.flip()


    def flip_stock(self):
        if len(self.stock) == 0:
            self._transfer_cards('talon', 'stock', len(self.piles['talon']))
            self._flip_deck('stock')
        #    self.talon, self.stock = deal(self.talon, self.stock, len(self.talon))
        #    flip_deck(self.stock)
        
        self._flip_deck('stock')
        self._transfer_cards('stock', 'talon', 1)
        #self.stock, self.talon = deal(self.stock, self.talon, 1)
        self._flip_deck('stock')
        return

    def check_tableau(self):
        for x in range(7):
            if len(self.piles[('tableau', x)]) > 0 and not self.piles[('tableau', x)][0].visible:
                self.piles[('tableau', x)][0].flip()


    def move(self, source, dest):
        tableaus = [('tableau', x) for x in range(7)]
        foundations = [('foundation', x) for x in range(4)]
        
        #from: talon or tableaus
        #to: tableaus or foundation
        if dest in tableaus:
            if source == 'talon':
                break # validate single card move
            elif source in tableaus:
                break # validate move and count cards to move
            else
                return False
        elif dest == 'foundation':
            if source == 'talon':
                break # validate move to foundation
            elif source in tableaus:
                break # validate move to foundation from this stack
            else
                return False
        else:
            return False
        return True

    def victory(self):
        foundations = [('foundation', x) for x in range(4)]
        complete_stacks = 0
        for foundation in foundations:
            if len(self.piles[foundation]) == 13:
                complete_stacks += 1
        if complete_stacks == 4:
            return True
        return False

    def _transfer_cards(self, source_key, dest_key, count, in_place=false):
        assert source_key, dest_key in self.piles.keys(), "Invalid pile keys"
        assert count < len(self.piles[source_key]), "Not enough cards in %s" % source_key

        if in_place: 
            self.piles[dest_key] = Deck(self.piles[source_key][:count] 
                                        + self.piles[dest_key][:])
        else:
            self.piles[dest_key] = Deck([card for card in reversed self.piles[source_key][:count]]
                                        + self.piles[dest_key][:])
        
        self.piles[source_key] = Deck(self.piles.[source_key][count:])
        return


    def _can_stack(self, top_card, base_card):
        if ((top_card.suit in self.suits[1:3]) and (base_card.suit not in self.suits[1:3])) or \
                ((top_card.suit not in self.suits[1:3]) and (base_card.suit in self.suits[1:3])):
            #If black on red or red on black
            if self.ranks.index(top_card.rank) \
                - self.ranks.index(base_card.rank) == -1:
                #And the new card is one lower than the old
                return True
        
        #Otherwise, the cards do not stack
        return False



            



def game_loop(game, menu_instructions):
    #Show game
    print(game)

    #game loop
    while True:
        print(menu_instructions)
        #Prompt for decision
        decision = input('> ').split()
        #for word in decision:
        #    print(word)
        #Validate input
        if len(decision) > 0:
            if decision[0] == 'm':
                game.move(('tableau', int(decision[1])-1), ('tableau', int(decision[2])-1))
                game.check_tableau()
            elif decision[0] == 'b':
                if decision[1] == 't':
                    game.move('talon', 'foundation')
                else:
                    game.move(('tableau', int(decision[1])-1), 'foundation')
                    game.check_tableau()
                if game.victory():
                    print("Yay you won!")
                    break
            elif decision[0] == 'p':
                game.move('talon', ('tableau', int(decision[1])-1))
            elif decision[0] == 'f':
                game.flip_stock()
            elif decision[0] == 'q':
                break
        #Perform action
        #Check for victory
        #Show game
        print(game)
        
    return

menu_instructions = ("Action Menu\n"
                     "---------------\n"
                     "- 'm [source] [dest]' to move from one tableau stack to another\n"
                     "- 'b [source]' to move from a stack to the foundations, [source] t for talon\n"
                     "- 'p'[dest] to move from the talon to a tableau stack\n"
                     "- 'f' to flip another card over from the stock\n"
                     "- 'q' to quit\n"
                    )


game = Solitaire()
game_loop(game, menu_instructions)


