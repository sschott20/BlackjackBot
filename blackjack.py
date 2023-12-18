import random
import itertools as it
import functools
# blackjack


@functools.total_ordering
class Card:
    def __init__(self, rank, suit):
        """ Creates a card of the given rank and suit.

            rank -- an integer
            suit -- a character
        """
        self._rank = rank
        self._suit = suit
        self._hash = str(self).__hash__()

    def rank(self):
        return self._rank

    def suit(self):
        return self._suit

    def same_suit(self, other):
        return self._suit == other._suit

    def __repr__(self):
        return "" + str(self._rank) + str(self._suit)

    def __eq__(self, other):
        return self._rank == other._rank

    def __lt__(self, other):
        return self.rank() < other.rank()

    def __hash__(self):
        return self._hash


class Deck:
    def __init__(self, ranks, suits, copies):
        """ Creates a deck of cards including the given number of copies
            of each possible combination of the given ranks and the
            given suits.

            ranks -- an iterable of integers
            suits -- an iterable
            copies -- a nonnegative integer
        """
        self._cards = []
        for copy in range(copies):
            self._cards.extend(
                map(lambda c: Card(*c), it.product(ranks, suits)))

    def shuffle(self):
        """ Shuffles this deck. """
        random.shuffle(self._cards)

    def size(self):
        """ Returns the number of cards remaining in this deck. """
        return len(self._cards)

    def deal(self, n):
        """ Removes and returns the next n cards from this deck.

            n -- an integer between 0 and the size of this deck (inclusive)
        """
        dealt = self._cards[-n:]
        dealt.reverse()
        del self._cards[-n:]
        return dealt


class Game:
    def __init__(self, shoe_size, bet_sizes):
        self.bet_sizes = bet_sizes
        self.shoe_size = shoe_size
        self.shuffle()
        self.state = self.initial_state()

    def all_ranks(self):
        return range(1, 14)

    def all_suits(self):
        return ['S', 'H', 'D', 'C']

    def shuffle(self):
        self.deck = Deck(self.all_ranks(), self.all_suits(), self.shoe_size)
        self.deck.shuffle()

    def initial_state(self):
        return Game.State([], [], self.deck, 0, 0, self.bet_sizes, self.shoe_size, True)

    def new_shoe(self):
        self.shuffle()
        self.state = Game.State(
            [], [], self.deck, 0, self.state.money, self.bet_sizes, self.shoe_size, True)

    class State:
        def __init__(self, player_hand, dealer_hand, deck: Deck, bet, money, bet_sizes, shoe_size, hand_over) -> None:
            self.player_hand = player_hand
            self.dealer_hand = dealer_hand
            self.deck = deck
            self.bet = bet
            self.money = money
            self.bet_sizes = bet_sizes
            self.shoe_size = shoe_size
            self.hand_over = hand_over

        def __str__(self):
            # return str(self.player_hand) + " " + str(self.dealer_hand) + " " + str(self.bet) + " " + str(self.money) + " " + str(self.bet_sizes[-1]) + " " + str(self.shoe_size) + " " + str(self.hand_over)
            return "---\nPlayer Hand: " + str(self.player_hand) + " " + str(self.score(self.player_hand)) + "\nDealer Hand: " + str(self.dealer_hand) + "\nBet: " + str(self.bet) + "\nMoney: " + str(self.money) + "\nBet Sizes: " + str(self.bet_sizes[-1]) + "\nShoe Size: " + str(self.shoe_size) + "\nHand Over: " + str(self.hand_over) + "\n---"

        def payoff(self):
            if not self.hand_over:
                return 0
            player_score = self.score(self.player_hand)
            dealer_score = self.score(self.dealer_hand)
            # naturals
            if player_score == 21 and dealer_score != 21:
                if len(self.player_hand) == 2:
                    return 1.5 * self.bet
                else:
                    return self.bet
            elif player_score != 21 and dealer_score == 21:
                return -1 * self.bet
            elif player_score == 21 and dealer_score == 21:
                return 0
            elif player_score > 21:
                return -1 * self.bet
            elif dealer_score > 21:
                return self.bet
            elif player_score == dealer_score:
                return 0
            elif player_score > dealer_score:
                return self.bet
            else:
                return -1 * self.bet

        def get_actions(self):
            if self.hand_over:
                return self.bet_sizes
            else:
                return ['H', 'S']
        # def payoff(self):
        #     if self.hand_over:

        def successor(self, action):

            if action == 'H':
                self.player_hand += self.deck.deal(1)
                if self.score(self.player_hand) >= 21:
                    self.hand_over = True
                    while self.score(self.dealer_hand) < 17:
                        self.dealer_hand += self.deck.deal(1)
                return self
            elif action == 'S':
                self.hand_over = True
                while self.score(self.dealer_hand) < 17:
                    self.dealer_hand += self.deck.deal(1)
                return self
            elif int(action) in self.get_actions():
                self.bet = int(action)
                self.player_hand = self.deck.deal(2)
                self.dealer_hand = self.deck.deal(2)
                if self.score(self.player_hand) == 21 or self.score(self.dealer_hand) == 21:
                    self.hand_over = True
                else:
                    self.hand_over = False
                return self
            else:
                print("Invalid action")
                return self

        def score(self, hand):
            score = 0
            sorted_hand = sorted(hand, reverse=True)
            for card in sorted_hand:
                if card.rank() == 1:
                    if score + 11 > 21:
                        score += 1
                    else:
                        score += 11
                elif card.rank() > 10:
                    score += 10
                else:
                    score += card.rank()
            return score
