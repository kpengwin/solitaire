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


class Solitaire:
    def __init__(self):
        #set up card piles
        self.piles =       {('foundation', x)   :   Deck([])    for x in range(4) }
        self.piles.update( {('tableau', x)      :   Deck([])    for x in range(7) } )
        self.piles.update( {'talon'             :   Deck([]) } )
        self.piles.update( {'stock'             :   Deck() } )      #all cards start here

        #grab a local copy of these for simplicity
        self.suits = self.piles['stock'].suits
        self.ranks = self.piles['stock'].ranks

        #prep cards
        self.piles['stock'].shuffle()
        for x in range(7):
            self._transfer_cards('stock', ('tableau', x), x)
            self._flip_deck(('tableau', x))
            self._transfer_cards('stock', ('tableau', x), 1)
        self._flip_deck('stock') 


    def __str__(self):
        desc = ''
        tableaus = [('tableau', x) for x in range(7)]
        foundations = [('foundation', x) for x in range(4)]

        desc += 'Foundations\n'
        for pile in foundations:
            desc += self.suits[pile[1]] + ' foundation.\n'
            for card in self.piles[pile]:
                desc += '%s\n' % card
            desc += '\n'
        desc += '\n'

        desc += 'Stock\n'
        for card in self.piles['stock']:
            desc += '%s\n' % card

        desc += '\nTalon\n'
        for card in self.piles['talon']:
            desc += '%s\n' % card

        desc += '\n'
        index = 0
        for pile in tableaus:
            count = 0
            desc += 'Tableau Pile %i\n' % (pile[1] + 1)
            for card in self.piles[pile]:
                if card.visible:
                    desc += '%s\n' % card
                else:
                    count +=1
            if count:
                desc += 'Upside down cards (%i)\n' % count
            desc += '\n'
        return desc


    def _flip_deck(self, deck_key):
        assert deck_key in self.piles.keys(), "Can't flip, invalid pile."
        for card in self.piles[deck_key]:
            card.flip()

    
    def _transfer_cards(self, source_key, dest_key, count, in_place=False):
        assert source_key in self.piles.keys(), "Invalid pile keys"
        assert dest_key in self.piles.keys(), "Invalid pile keys"
        assert count <= len(self.piles[source_key]), "Not enough cards in pile"

        if in_place: 
            self.piles[dest_key] = Deck(self.piles[source_key][:count] 
                                        + self.piles[dest_key][:])
        else:
            self.piles[dest_key] = Deck([card for card in reversed(self.piles[source_key][:count])]
                                        + self.piles[dest_key][:])
        
        self.piles[source_key] = Deck(self.piles[source_key][count:])
        return


    def _can_stack(self, top_card, base_card):
        reds    = self.suits[1:3]
        blacks  = [self.suits[0], self.suits[3]]
        if ((top_card.suit in reds) and (base_card.suit in blacks)) or \
                ((top_card.suit in blacks) and (base_card.suit in reds)):
            #If black on red or red on black
            if self.ranks.index(top_card.rank) \
                - self.ranks.index(base_card.rank) == -1:
                #And the new card is one lower than the old
                return True
        
        #Otherwise, the cards do not stack
        return False


    def flip_stock(self):
        if len(self.piles['stock']) == 0:
            self._transfer_cards('talon', 'stock', len(self.piles['talon']))
            self._flip_deck('stock')
        
        self._flip_deck('stock')
        self._transfer_cards('stock', 'talon', 1)
        self._flip_deck('stock')
        return


    def check_tableau(self):
        for x in range(7):
            if len(self.piles[('tableau', x)]) > 0 and not self.piles[('tableau', x)][0].visible:
                self.piles[('tableau', x)][0].flip()


    def move(self, source, dest):
        tableaus = [('tableau', x) for x in range(7)]
        foundations = [('foundation', x) for x in range(4)]
        if (source not in self.piles.keys()) or (not len(self.piles[source])):
            return False

        #from: talon or tableaus
        #to: tableaus or foundation
        if dest in tableaus:
            if source == 'talon':
                if len(self.piles[dest]):
                    if self._can_stack(self.piles[source][0], self.piles[dest][0]):
                        self._transfer_cards(source, dest, 1)
                    else:
                        return False
                elif not (len(self.piles[dest]) and self.piles[source][0].rank == 'K'):
                    self._transfer_cards(source, dest, 1)
                else:
                    return False
            elif source in tableaus:
                transfer_depth = 0
                valid_transfer = False
                for card in self.piles[source]:
                    transfer_depth += 1
                    if card.visible == False:
                        transfer_depth = 0
                        break
                    elif len(self.piles[dest]) == 0:
                        if (card.rank == 'K'):
                            valid_transfer = True
                            break
                    elif self._can_stack(card, self.piles[dest][0]):
                        valid_transfer = True
                        break
                if valid_transfer:
                    self._transfer_cards(source, dest, transfer_depth, in_place=True)
                else:
                    return False
            else:
                return False
        elif dest == 'foundation':
            if (source == 'talon' or source in tableaus):
                card = self.piles[source][0]
                foundation_height = len(self.piles[('foundation', self.suits.index(card.suit))]) - 1
                if self.ranks.index(card.rank) - 1 == foundation_height:
                    self._transfer_cards(source, ('foundation', self.suits.index(card.suit)), 1)
                else:
                    return False
            else:
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


## end of classes


def game_loop(game, menu_instructions):
    #Show game
    print(game)

    #game loop
    while True:
        print(menu_instructions)
        #Prompt for decision
        decision = input('> ').split()
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


