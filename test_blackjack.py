from blackjack import *


if __name__ == "__main__":
    game = Game(6, [i for i in range(1, 10)])
    position = game.initial_state()
    print(position)
    # print(position.get_actions())
    position = position.successor(6)
    while not position.hand_over:
        position = position.successor('H')
        print(position)
    print(position)
