from blackjack import *
import sys
import argparse
import time
import mcts
import qlearn

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blackjack Bot")
    parser.add_argument('--count', dest='count', type=int, action="store",
                        default=1, help='number of shoes to play (default=1)')
    parser.add_argument('--time', dest='time', type=float,
                        action="store", default=0.1, help='time allowed per move')
    parser.add_argument('--model', dest="model", choices=[
                        "user", "always_hit", "always_stand", "hit_until", "mcts", "qlearn"], default="basic", help="model to use")
    parser.add_argument('--shoe_size', dest="shoe_size", type=int,
                        default=6, help="number of decks in shoe")
    parser.add_argument("--pen ", dest="pen", type=int,
                        default=6, help="percentage of shoe to reshuffle")
    parser.add_argument("--display", dest="display", action="store_true")

    args = parser.parse_args()
    game = Game(args.shoe_size, [i for i in range(1, 10, 3)])
    if args.model == "user":
        predict = user_mode
    elif args.model == "always_stand":
        predict = always_stand
    elif args.model == "always_hit":
        predict = always_hit
    elif args.model == "hit_until":
        predict = hit_until
    elif args.model == "mcts":
        predict = mcts.mcts_policy(args.time)
    elif args.model == "qlearn":
        predict = qlearn.qlearn_policy(game, args.time)
    # print([i for i in range(1, 11, 3)])
    num_hands = 0

    for i in range(args.count):
        # print("Shoe " + str(i + 1) + " of " + str(args.count))
        game.shuffle()
        game.new_shoe()
        while game.deck.size() > (args.shoe_size * 52) / 6:
            # print(game.deck.size())
            num_hands += 1
            bet = predict(game.state)
            game.state.update_game(bet)
            while not game.state.hand_over:
                # print(game.state, game.deck.size())

                action = predict(game.state)
                if args.display:
                    print(game.state.player_hand,
                          game.state.score(game.state.player_hand))
                    print([game.state.dealer_hand[0]])
                    print("Action: " + str(action))
                game.state.update_game(action)

                if game.state.hand_over:
                    payoff = game.state.payoff()
                    game.state.money += payoff
                    if args.display:
                        print("Hand over")
                        print("Player got a " + str(game.state.player_hand) +
                              " for a score of ", game.state.score(game.state.player_hand))
                        print("Dealer got a " + str(game.state.dealer_hand) +
                              " for a score of ", game.state.score(game.state.dealer_hand))
                        if payoff > 0:
                            print("You won " + str(payoff))
                        elif payoff == 0:
                            print("You tied, bet of " +
                                  str(game.state.bet) + " returned")
                        else:
                            print("You lost " + str(game.state.bet))
                        input("Current balance: " +
                              str(game.state.money) + "\n")
    print("Money: $" + str(game.state.money))
    print("Hands: " + str(num_hands))
    print("Money per hand: $" + str(game.state.money / num_hands))
