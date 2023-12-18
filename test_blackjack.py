from blackjack import *
import sys
import argparse
import time
import mcts
import xmax


def always_stand(state):
    if state.hand_over:
        return 1
    else:
        return "S"


def always_hit(state):
    if state.hand_over:
        return 1
    else:
        return "H"


def hit_until(state):
    if state.hand_over:
        return 1
    else:
        if state.score(state.player_hand) < 17:
            return "H"
        else:
            return "S"


def user_mode(state):
    print()
    if not state.hand_over:
        print(state.player_hand, state.score(state.player_hand))
        print([state.dealer_hand[0]])
    print(state.get_actions())
    action = input("What would you like to do?\n")
    if action == 'H' or action == 'h':
        return 'H'
    elif action == 'S' or action == 's':
        return 'S'
    elif int(action) in state.get_actions():
        return int(action)
    return action

predict = xmax.xmax_policy()
game = Game(1, [i for i in range(1, 10, 3)])
predict(game.state)

