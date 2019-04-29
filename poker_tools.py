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
    deck = deque([])

    def __init__(self):
        ranks = {'a': 'Ace', 'k': 'King', 'q': 'Queen', 'j': 'Jack', '10': 'Ten', '9': 'Nine', '8': 'Eight',
                 '7': 'Seven', '6': 'Six', '5': 'Five', '4': 'Four', '3': 'Three', '2': 'Two'}
        # Possible suits: clubs (♣), diamonds ( ), hearts (♥) and spades (♠)
        suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
        for r in ranks:
            for s in suits:
                self.deck.append(Card(ranks[r], suits[s]))

    def __str__(self):
        st = ''
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


class Player(object):
    """Definition of the Player Object.\n
        Represents a player of a Texas Holdem game."""

    def __init__(self, name, bankroll):
        self.name = str(name)
        self.bet_size = 0
        self.hand = []
        self.bankroll = bankroll

    def __str__(self):
        return self.name

    def clear_hand(self):
        self.hand = []

    def get_hand(self, deck):
        self.hand = []
        self.hand.append(deck.deal())
        self.hand.append(deck.deal())

    def place_bet(self, size):
        if size == "all in" or size > self.bankroll:
            self.bet_size = self.bankroll
            self.bankroll = 0
        else:
            self.bet_size = size
            self.bankroll -= self.bet_size
        return self.bet_size


class Table(object):
    """Definition of the Table Object.\n
        Represents the set-up of a game of Texas Holdem."""
    common_cards = []
    players_in_game = []
    deck = Deck()
    pot = 0
    max_bet = 0

    def __init__(self, *players):
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


class Evaluator(object):
    """Definition of the Evaluator Object.\n
        This is a helping object to evaluate final outcomes.\n
        (Not sure if it is needed yet)"""
    suits = {'h': 'Heart', 'd': 'Diamond', 's': 'Spade', 'c': 'Club'}
    best_hand = []
    result = 'High Card'
    score = 0

    def create_ordered_hand(*five_cards):
        order = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        hand = list(five_cards)
        hand.sort(key=lambda x: order.index(x.rank))
        return hand

    def straight(*five_ordered_cards):
        if five_ordered_cards[-1].suit == 'Ace' and five_ordered_cards[0].suit == 'Two' \
                and five_ordered_cards[1].suit == 'Three' and five_ordered_cards[2].suit == 'Four' \
                and five_ordered_cards[3].suit == 'Five':
            return True

        order = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        start = order.index(five_ordered_cards[0].suit)
        for i in range(1, 5):
            if order.index(five_ordered_cards[i].suit) != start+i:
                return False
        return True

    def flush(*five_ordered_cards):
        for card in five_ordered_cards:
            if card.suit != five_ordered_cards[0].suit:
                return False
        return True

    def one_pair(*five_ordered_cards):
        for i in range(4):
            if five_ordered_cards[i].rank == five_ordered_cards[i + 1].rank:
                return True
        return False

    def two_pairs(*five_ordered_cards):
        if five_ordered_cards[0].rank == five_ordered_cards[1].rank:
            if five_ordered_cards[2].rank == five_ordered_cards[3].rank or \
                            five_ordered_cards[3].rank == five_ordered_cards[4].rank:
                return True
        if five_ordered_cards[1].rank == five_ordered_cards[2].rank \
                and five_ordered_cards[3].rank == five_ordered_cards[4].rank:
            return True
        return False

    def three_of_kind(*five_ordered_cards):
        for i in range(3):
            if five_ordered_cards[i].rank == five_ordered_cards[i + 1].rank \
                    and five_ordered_cards[i].rank == five_ordered_cards[i + 2].rank:
                return True
        return False

    def four_of_kind(*five_ordered_cards):
        for i in range(2):
            if five_ordered_cards[i].rank == five_ordered_cards[i + 1].rank \
                    and five_ordered_cards[i].rank == five_ordered_cards[i + 2].rank \
                    and five_ordered_cards[i].rank == five_ordered_cards[i + 3].rank:
                return True
        return False

    def full_house(*five_ordered_cards):
        if five_ordered_cards[0].rank == five_ordered_cards[1].rank \
                and five_ordered_cards[3].rank == five_ordered_cards[4].rank:
            if five_ordered_cards[0].rank == five_ordered_cards[2].rank \
                    or five_ordered_cards[2].rank == five_ordered_cards[3].rank:
                return True
        return False

    def hand_evaluator(self, *five_cards):
        order = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
        answer = [None, None]
        cards = self.create_ordered_hand(five_cards)
        if self.straight(cards) and self.flush(cards):
            if cards[-1].rank == 'Ace' and cards[-2].rank == 'King':
                answer[0] = 'Royal Flush'
            elif cards[-1].rank == 'Ace':
                answer[0] = 'Straight Flush'
                answer[1] = order.index('Five')
            else:
                answer[0] = 'Straight Flush'
                answer[1] = order.index(cards[-1].rank)
            return answer
        if self.four_of_kind(cards):
            answer[0] = 'Four of a Kind'
            answer[1] = order.index(five_cards[2].rank)
            return answer
        if self.full_house(cards):
            answer[0] = 'Full House'
            answer[1] = 100*order.index(five_cards[2].rank) + (
                    order.index(five_cards[0].rank) + order.index(five_cards[4].rank) -
                    order.index(five_cards[2].rank))  # The parenthesis gives the index of the rank from pair.
            return answer
        if self.flush(cards):
            answer[0] = 'Flush'
            answer[1] = order.index(cards[-1].rank)
            return answer
        if self.straight(cards):
            answer[0] = 'Straight'
            if cards[0].rank == 'Two' and cards[-1].rank == 'Ace':
                answer[1] = order.index('Five')
            else:
                answer[1] = order.index(cards[-1].rank)
                return answer
        if self.three_of_kind(cards):
            answer[0] = 'Three of a King'
            answer[1] = order.index(five_cards[2].rank)  # The middle card belongs always to the triple.
            return answer
        if self.two_pairs(cards):
            answer[0] = 'Two Pairs'
            if cards[-1].rank == cards[-2]:
                answer[1] = 100*order.index(cards[-1].rank) + order.index(cards[1].rank)
            else:
                answer[1] = 100*order.index(cards[2].rank) + order.index(cards[0].rank)
            return answer
        if self.one_pair(cards):
            answer[0] = 'One Pair'
            for i in range(4):
                if cards[i].rank == cards[i+1].rank:
                    answer[1] = order.index(cards[i].rank)
            return answer
        answer = ['High Card', order.index(cards[-1])]
        return answer

    def evaluate(self, *hand_combined_with_common):
        ranking = {'Royal Flush': 9, 'Straight Flush': 8, 'Four of a Kind': 7, 'Full House': 6, 'Straight': 4,
                   'Flush': 5, 'Three of a King': 3, 'Two Pairs': 2, 'One Pair': 1, 'High Card': 0}
        seven_cards = list(hand_combined_with_common)
        for i in range(6):
            for j in range(i + 1, 7):
                temp_hnd = seven_cards.copy()
                temp_hnd.remove(seven_cards[i])
                temp_hnd.remove(seven_cards[j])
                [tmp_result, tmp_score] = self.hand_evaluator(temp_hnd)
                if ranking[tmp_result] > ranking[self.result]:
                    self.result = tmp_result
                    self.score = tmp_score
                if tmp_result == self.result and self.score < tmp_score:
                    self.score = tmp_score


if __name__ == "__main__":
    o = Deck()
    print(o)
    print(o.deal())
