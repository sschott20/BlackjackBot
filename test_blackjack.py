from blackjack import *
import sys 
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test MCTS agent")
    parser.add_argument('--count', dest='count', type=int, action="store", default=2, help='number of games to play (default=2')
    parser.add_argument('--time', dest='time', type=float, action="store", default=0.1, help='time for MCTS per move')
    parser.add_argument('--depth', dest='depth', type=int, action='store', default=2, help='depth of minimax search to compare MCTS to (default=2)')
    parser.add_argument('--random', dest="p_random", type=float, action="store", default = 0.0, help="p(random instead of minimax) (default=0.0)")
    parser.add_argument('--game', dest="game", choices=["kalah", "pegging", "pegging-5"], default="pegging", help="game to play")

    game = Game(6, [i for i in range(1, 10)])
    position = game.initial_state()
    # print(position.get_actions())
    position = position.successor(6)
    print(position)
    while not position.hand_over:
        position = position.successor('H')
        print(position)
    print(position.payoff())
