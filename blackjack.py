import random
from Deck import Card, Deck

# class to represent a game of blackjack


class Game:
    def __init__(self, copies):
        self.copies = copies
        self.shuffle()
        self.hand = []
        self.bet = -1

    def shuffle(self):
        self.deck = Deck(range(2, 15), ['C', 'D', 'H', 'S'], self.copies)
        self.deck.shuffle()

    def deal(self, bet):
        self.bet = bet
        return self.deck.deal(2)

    def hit(self):
        # returns (outcome, total)
        # outcome -1 if bust, 0 otherwise
        # total is the total of the hand

        self.hand.append(self.deal(1)[0])
        total = self.tally()
        if total > 21:
            return (-1, total)
        else:
            return (0, total)

    def tally(self):
        total = 0
        sorted_hand = sorted(self.hand, key=lambda c: c.rank())
        for card in sorted_hand:
            if card.rank() == 14:
                if total + 11 > 21:
                    total += 1
                else:
                    total += 11
            elif card.rank() > 10:
                total += 10
            else:
                total += card.rank()

        return total
