#! /usr/bin/python3.5.2


class Card(object):

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):
    from collections import deque
    deck = deque([])

    def __init__(self):
        ranks = {'a': 'Ace', 'k': 'King', 'q': 'Queen', 'j': 'Jack', '10': 'Ten', '9': 'Nine', '8': 'Eight',
                 '7': 'Seven', '6': 'Six', '5': 'Five', '4': 'Four', '3': 'Three', '2': 'Two'}
        # clubs (♣), diamonds ( ), hearts (♥) and spades (♠)
        suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
        for r in ranks:
            for s in suits:
                self.deck.append(Card(ranks[r], suits[s]))

    def __str__(self):
        for i in self.deck:
            print(i)
        return ' '

    def shuffle(self):
        import random
        random.shuffle(self.deck)

    def deal(self):
        try:
            return self.deck.popleft()
        except IndexError:
            return None


class Player(object):
    bet = 0

    def __init__(self, name=None, bankroll=None):
        self.name = name
        self.hand = []
        self.bankroll = bankroll

    def __str__(self):
        return self.name

    def get_hand(self, deck):
        self.hand = []
        self.hand.append(deck.deal())
        self.hand.append(deck.deal())


class Table(object):
    common_cards = []
    players_in_game = []
    deck = Deck()
    pot = 0

    def __init__(self, *players):
        self.deck.shuffle()
        for pl in players:
            self.players_in_game.append(pl)

    def new_player(self, position, player):
        self.players_in_game.insert(position, player)

    def player_leaves(self, player):
        try:
            self.players_in_game.remove(player)
        except ValueError:
            pass

    def flop(self):
        self.common_cards.append(deck.deal())
        self.common_cards.append(deck.deal())
        self.common_cards.append(deck.deal())

    def turn(self):
        self.common_cards.append(deck.deal())

    def river(self):
        self.common_cards.append(deck.deal())

    def end_turn(self, shuffle=True):
        self.common_cards = []
        self.pot = 0
        self.deck = Deck()
        if shuffle:
            self.deck.shuffle()



class Texas(object):
    pass




d = Deck()
p = Player("John")
print(d)
print(p)
print(p.hand)
p.get_hand(d)
print(p.hand)
