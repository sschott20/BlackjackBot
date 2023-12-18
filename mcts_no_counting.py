import time
import math
import random
import blackjack
import copy
EXPLORATION_CONSTANT = 2


def simulate(state):
    while (not state.hand_over):
        state = state.successor(random.choice(state.get_actions()))
    return state.payoff()


def weight(reward, visits, total):
    if visits == 0:
        return 999999
    return ((reward / visits) + math.sqrt((EXPLORATION_CONSTANT * math.log(total)) / visits))


def mcts(state, d, is_start):
    # if state is terminal, return reward
    # state_hash = hash(state)
    if state.hand_over and not is_start:
        return state.payoff()
    state_hash = hash(state)
    # print(state_hash)
    # print(state)
    # otherwise choose the action with max weight
    actions = state.get_actions()
    total = 0
    sim = False
    for s in actions:
        if (state_hash, s) not in d:
            d[(state_hash, s)] = [0, 0]
            sim = True
        else:
            total += d[(state_hash, s)][1]

    weights = []

    for s in actions:
        reward, visits = d[(state_hash, s)]
        weights.append(weight(reward, visits, total))
    action = actions[weights.index(max(weights))]

    if sim:
        reward = simulate(state.successor(action))
    else:
        reward = mcts(state.successor(action), d, False)

    d[(state_hash, action)][0] += reward
    d[(state_hash, action)][1] += 1

    return reward


def mcts_policy(time_limit):
    d = {}

    def mcts_wrapper(start_state):
        start = time.time()

        actions = start_state.get_actions()
        start_hash = hash(start_state)
        for s in actions:
            if (start_hash, s) not in d:
                d[(start_hash, s)] = [0, 0]
        # print(hash(start_state))
        while time.time() - start < time_limit:
            # print(d)
            # print(start_state.deck.size())
            tmp_state = copy.deepcopy(start_state)
            tmp_state.deck = blackjack.Deck(
                range(1, 14), ['S', 'H', 'D', 'C'], 6)
            mcts(tmp_state, d, True)
        scores = []

        # print(d)
        for s in actions:
            reward, visits = d[(start_hash, s)]
            # print((start_hash, s), reward, visits)
            scores.append(reward / visits)

        global EXPLORATION_CONSTANT
        EXPLORATION_CONSTANT = max(
            abs(max(scores) - min(scores)), EXPLORATION_CONSTANT)

        return actions[scores.index(max(scores))]

    return mcts_wrapper
