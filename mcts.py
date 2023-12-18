import time
import math
import random
import blackjack

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
    if state.hand_over and not is_start:
        return state.payoff()

    # otherwise choose the action with max weight
    actions = state.get_actions()
    total = 0
    sim = False
    for s in actions:
        if (state, s) not in d:
            d[(state, s)] = [0, 0]
            sim = True
        else:
            total += d[(state, s)][1]

    weights = []
    for s in actions:
        reward, visits = d[(state, s)]
        weights.append(weight(reward, visits, total))
    action = actions[weights.index(max(weights))]

    if sim:
        reward = simulate(state.successor(action))
    else:
        reward = mcts(state.successor(action), d, False)
    # if (state, action) not in d:
    #     print(state, action)
    print(d)
    d[(state, action)][0] += reward
    d[(state, action)][1] += 1

    return reward


def mcts_policy(time_limit):
    d = {}

    def mcts_wrapper(start_state):
        start = time.time()

        actions = start_state.get_actions()
        for s in actions:
            if s not in d:
                d[(start_state, s)] = [0, 0]

        while time.time() - start < time_limit:
            mcts(start_state, d, True)
        scores = []
        for s in actions:
            reward, visits = d[(start_state, s)]
            scores.append(reward / visits)

        global EXPLORATION_CONSTANT
        EXPLORATION_CONSTANT = max(
            abs(max(scores) - min(scores)), EXPLORATION_CONSTANT)

        if start_state.actor() == 0:
            return actions[scores.index(max(scores))]
        else:
            return actions[scores.index(min(scores))]

    return mcts_wrapper
