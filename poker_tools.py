from random import shuffle, choice
from collections import deque


class Card(object):
    """Definition of the Card Object.\n
        Represents a card from a normal deck."""

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck(object):
    """Definition of the Deck Object.\n
        Represents a normal deck for playing cards."""

    def __init__(self):
        ranks = {'a': 'Ace', 'k': 'King', 'q': 'Queen', 'j': 'Jack', '10': 'Ten', '9': 'Nine', '8': 'Eight',
                 '7': 'Seven', '6': 'Six', '5': 'Five', '4': 'Four', '3': 'Three', '2': 'Two'}
        # Possible suits: clubs (♣), diamonds ( ), hearts (♥) and spades (♠)
        suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
        self.deck = deque([])
        for r in ranks:
            for s in suits:
                self.deck.append(Card(ranks[r], suits[s]))

    def __str__(self):
        st = 'There are {} cards remaining:\n'.format(len(self.deck))
        for i in self.deck:
            st += str(i) + "\n"
        return st

    def shuffle(self):
        shuffle(self.deck)

    def deal(self):
        try:
            return self.deck.popleft()
        except IndexError:
            return None


class Hand(object):

    """Definition of the Hand Object.\n
        This is a helping object to evaluate final outcomes.\n
        (Not sure if it is needed yet)"""

    suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
    best_hand = []
    result = 'High Card'
    score = 0

    _order = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
    _rankings = ['High Card', 'Pair', 'Two pair', 'Three of a kind', 'Straight', 'Flush', 'Full house',
                 'Four of a kind', 'Straight flush', 'Royal flush']

    def __init__(self, cards):
        self.cards = cards
        weights = {}
        for card in self.cards:
            if card.rank in weights:
                weights[card.rank] += 1
            else:
                weights[card.rank] = 1
        self.cards.sort(key=lambda x: (weights[x.rank], self._order.index(x.rank)), reverse=True)
        self.hand = self.get_result()

    def __str__(self):
        return "[ {}, {}, {}, {}, {}]".format(self.cards[0], self.cards[1], self.cards[2], self.cards[3], self.cards[4])

    def __lt__(self, other):  # For x < y
        if self._rankings.index(self.hand) < self._rankings.index(other.hand):
            return True
        elif self._rankings.index(self.hand) == self._rankings.index(other.hand):
            for i in range(5):
                if self._order.index(self.cards[i].rank) < self._order.index(other.cards[i].rank):
                    return True
                elif self._order.index(self.cards[i].rank) > self._order.index(other.cards[i].rank):
                    return False
        return False

    def __eq__(self, other):  # For x == y
        if isinstance(other, self.__class__):
            for i in range(5):
                if self.cards[i].rank != other.cards[i].rank:
                    return False
            return self._rankings.index(self.hand) == self._rankings.index(other.hand)
        return False

    def __le__(self, other):  # For x <= y
        return self < other or self == other

    def __ne__(self, other):  # For x != y OR x <> y
        return not self == other

    def __gt__(self, other):  # For x > y
        return other < self

    def __ge__(self, other):  # For x >= y
        return other < self or self == other

    def get_result(self):
        if self.straight() and self.flush():
            if self.cards[1].rank == 'King':
                return 'Royal flush'
            else:
                return 'Straight flush'
        elif self.four_of_kind():
            return 'Four of a kind'
        elif self.full_house():
            return 'Full house'
        elif self.flush():
            return 'Flush'
        elif self.straight():
            return 'Straight'
        elif self.three_of_kind():
            return 'Three of a kind'
        elif self.two_pairs():
            return 'Two pair'
        elif self.one_pair():
            return 'Pair'
        else:
            return 'High Card'

    def straight(self):
        if self.cards[0].suit == 'Ace' and self.cards[4].suit == 'Two' and self.cards[3].suit == 'Three' and \
                self.cards[2].suit == 'Four' and self.cards[1].suit == 'Five':
            return True

        for i in range(0, 4):
            if self._order.index(self.cards[i].rank) != self._order.index(self.cards[i+1].rank)+1:
                return False
        return True

    def flush(self):
        for card in self.cards:
            if card.suit != self.cards[0].suit:
                return False
        return True

    def one_pair(self):
        for i in range(4):
            if self.cards[i].rank == self.cards[i+1].rank:
                return True
        return False

    def two_pairs(self):
        if self.cards[0].rank == self.cards[1].rank:
            if self.cards[2].rank == self.cards[3].rank or self.cards[3].rank == self.cards[4].rank:
                return True
        if self.cards[1].rank == self.cards[2].rank and self.cards[3].rank == self.cards[4].rank:
            return True
        return False

    def three_of_kind(self):
        for i in range(3):
            if self.cards[i].rank == self.cards[i+1].rank and self.cards[i+1].rank == self.cards[i+2].rank:
                return True
        return False

    def four_of_kind(self):
        for i in range(2):
            if self.cards[i].rank == self.cards[i+1].rank and self.cards[i+1].rank == self.cards[i+2].rank \
                    and self.cards[i+2].rank == self.cards[i+3].rank:
                return True
        return False

    def full_house(self):
        if self.cards[0].rank == self.cards[1].rank and self.cards[3].rank == self.cards[4].rank:
            if self.cards[1].rank == self.cards[2].rank or self.cards[2].rank == self.cards[3].rank:
                return True
        return False


class Player(object):
    """Definition of the Player Object.\n
        Represents a player of a Texas Holdem game."""

    def __init__(self, name, bankroll):
        self.name = str(name)
        self.bet_size = 0
        self.hole_cards = []
        self.bankroll = bankroll
        self.hand = None

    def __str__(self):
        return self.name

    def clear_hole_cards(self):
        self.hole_cards = []

    def get_hole_cards(self, deck):
        self.clear_hole_cards()
        self.hole_cards.append(deck.deal())
        self.hole_cards.append(deck.deal())

    def place_bet(self, size):
        if size == "all in" or size > self.bankroll:
            self.bet_size = self.bankroll
            self.bankroll = 0
        else:
            self.bet_size = size
            self.bankroll -= self.bet_size
        return self.bet_size

    def get_best_hand(self, lst):
        if len(self.hole_cards) != 2 or len(lst) != 5:
            raise ValueError("Not the correct number of cards were given.")
        seven_cards = self.hole_cards+lst
        self.hand = Hand(seven_cards[2:])
        for i in range(0, 6):
            for j in range(i+2, 7):
                temp_hand = Hand([seven_cards[k] for k in range(7) if k != i and k != j])
                if self.hand < temp_hand:
                    self.hand = temp_hand


class Table(object):
    """Definition of the Table Object.\n
        Represents the set-up of a game of Texas Holdem."""
    common_cards = []
    players_in_game = []
    deck = Deck()
    pot = 0
    max_bet = 0

    def __init__(self, players):
        self.deck.shuffle()
        for pl in players:
            self.players_in_game.append(pl)
        self.small_blind = choice(self.players_in_game)
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

    def new_round(self):
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

    def play_game(self):
        pass


class Game(object):

    def __init__(self, main_player, number_of_players):
        # Here we should read from a yalm file the tournament definition
        main_player = Player(main_player, 1500)
        players_for_table = []
        for i in range(1, number_of_players):
            pass


if __name__ == "__main__":
    o = Deck()
    o.shuffle()
    print(o)
    hand1 = Hand([o.deal(), o.deal(), o.deal(), o.deal(), o.deal()])
    print(hand1)
    # print(hand.straight())
    print(hand1.hand)
    hand2 = Hand([o.deal(), o.deal(), o.deal(), o.deal(), o.deal()])
    print(hand2)
    print(hand2.hand)
    print(hand1 < hand2)
    print(hand1 <= hand2)
    print(hand1 == hand2)
    plr = Player("Alex", 0)
    plr.get_hole_cards(o)
    cards = [o.deal(), o.deal(), o.deal(), o.deal(), o.deal()]
    plr.get_best_hand(cards)
    print(plr.hole_cards[0], '-', plr.hole_cards[1], '-', cards[0], '-', cards[1], '-', cards[2], '-', cards[3], '-', cards[4])
    print(plr.hand)
    print(plr.hand.hand)
