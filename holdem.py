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


class Player(Evaluator):
    bet_size = 0

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
    order = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
    suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
    best_combination = []
    result = 0
    score = 0

    def create_ordered_hand(self, *five_cards):
        self.best_combination = five_cards.copy()
        self.best_combination.sort(key=lambda x: self.order.index(x.rank))

    def straight(self):
        if self.best_combination[-1].suit == 'Ace' and self.best_combination[0].suit == 'Two' \
                and self.best_combination[1].suit == 'Three' and self.best_combination[2].suit == 'Four' \
                and self.best_combination[3].suit == 'Five':
            self.score = 3  # highest card is order[3] == 'Five'
            return True
        start = self.order.index(self.best_combination[0].suit)
        for i in range(1, 5):
            if self.order.index(self.best_combination[i].suit) != start+i:
                return False
        return True

    def flush(self):
        for card in self.best_combination:
            if card.suit != self.best_combination[0].suit:
                return False
        return True

    def one_pair(self):
        for i in range(4):
            if self.best_combination[i].suit == self.best_combination[i + 1].suit:
                return True
        return False

    def two_pairs(self):
        if self.best_combination[0].suit == self.best_combination[1].suit:
            if self.best_combination[2].suit == self.best_combination[3].suit or \
                            self.best_combination[3].suit == self.best_combination[4].suit:
                return True
        if self.best_combination[1].suit == self.best_combination[2].suit \
                and self.best_combination[0].suit == self.best_combination[1].suit:
            return True
        return False

    def three(self):
        for i in range(3):
            if self.best_combination[i].suit == self.best_combination[i + 1].suit \
                    and self.best_combination[i].suit == self.best_combination[i + 2].suit:
                return True
        return False

    def full_house(self):
        if self.best_combination[0].suit == self.best_combination[1].suit \
                and self.best_combination[3].suit == self.best_combination[4].suit:
            if self.best_combination[0].suit == self.best_combination[2].suit \
                    or self.best_combination[0].suit == self.best_combination[3].suit:
                return True
        return False

    def evaluate(self, *hand_combined_with_common):
        for i in range(6):
            for j in range(i + 1, 7):
                temp_hnd = hand_combined_with_common.copy()
                temp_hnd.remove(hand_combined_with_common[i])
                temp_hnd.remove(hand_combined_with_common[j])
                self.create_ordered_hand(temp_hnd)

                if self.score <

                print(temp_hnd)



d = Deck()
p = Player("John")
print(d)
print(p)
print(p.hand)
p.get_hand(d)
print(p.hand)
