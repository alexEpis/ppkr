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
    max_bet = 0

    def __init__(self, *players):
        import random
        self.deck.shuffle()
        for pl in players:
            self.players_in_game.append(pl)
        self.small_blind = random.choice(self.players_in_game)
        self.big_blind = self.next_player(self.small_blind)
        self.current_player = self.next_player(self.big_blind)

    def next_player(self, player):
        try:
            inx = self.players_in_game.index(player)
            return self.players_in_game[inx + 1]
        except IndexError:
            return self.players_in_game[0]

    def new_player(self, position, player):
        self.players_in_game.insert(position, player)

    def player_leaves_table(self, player):
        try:
            self.players_in_game.remove(player)
        except ValueError:
            pass

    def flop(self):
        self.common_cards.append(self.deck.deal())
        self.common_cards.append(self.deck.deal())
        self.common_cards.append(self.deck.deal())

    def turn(self):
        self.common_cards.append(self.deck.deal())

    def river(self):
        self.common_cards.append(self.deck.deal())

    def begin_round(self):
        self.small_blind = self.big_blind
        self.big_blind = self.next_player(self.small_blind)
        self.current_player = self.next_player(self.big_blind)

    def end_round(self):
        self.common_cards = []
        self.pot = 0

    def bet(self, player, amount):
        if player.bankroll >= player.bet:
            player.bet += amount
            player.bankroll -= amount
        else:
            player.bet += player.bankroll
            player.bankroll = 0
        if player.bet > self.max_bet:
            self.max_bet = player.bet
            self.current_player = player


class Texas(object):
    pass


class Evaluator(object):
    order = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King']
    suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}

    def straight(self, *five_cards):
        cards = [x.rank for x in five_cards]
        cards.sort(key=lambda x: self.index(x[0]))
        pass

    def evaluate(self, *hand_combined_with_common):
        for i in range(6):
            for j in range(i + 1, 7):
                temp_hnd = hand_combined_with_common.copy()
                temp_hnd.remove(hand_combined_with_common[i])
                temp_hnd.remove(hand_combined_with_common[j])
                print(temp_hnd)



d = Deck()
p = Player("John")
print(d)
print(p)
print(p.hand)
p.get_hand(d)
print(p.hand)
