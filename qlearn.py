import time, random, copy, blackjack
LEARNING_RATE = 0.25
DISCOUNT_FACTOR = 0.99
EPSILON_START = 0.15
EPSILON_END = 0.01
EPSILON_DECAY = 0.995

def qlearn_policy(game, pen, time_limit):
    def get_action(state):
        if random.random() < epsilon:
            if len(state.player_hand) == 0 or state.hand_over:
                return actions[random.randint(len(postflop_actions), len(actions)-1)]
            else:
                return actions[random.randint(0, len(postflop_actions)-1)]
        else:
            return get_optimal_action(state)
    
    def calc_running_total(hand):
        total = 0
        for card in hand:
            if 2 <= card.rank() <= 6:
                total += 1
            elif card.rank() == 1:
                total -= 1
            elif 10 <= card.rank() <= 13:
                total -= 1
        return total
    
    def count_cards(running_count, state):
        player_hand = state.player_hand
        dealer_hand = state.dealer_hand
        if state.hand_over:
            if len(player_hand) > 2:
                running_count += calc_running_total(player_hand[2:])
            running_count += calc_running_total(dealer_hand[1:])
        else:
            running_count += calc_running_total(player_hand)
            running_count += calc_running_total(dealer_hand[0:1])
        decks_remaining = float(state.deck.size())/52
        true_count = running_count/decks_remaining
        return running_count, true_count, decks_remaining
    
    def check_ace(state):
        for card in state.player_hand:
            if card.rank() == 1:
                return 1
        return 0
    
    def find_key(superState, action):
        true_count, player_total, usable_ace, dealer_total = superState
        true_count_bucket = 0
        if true_count < -5:
            true_count_bucket = 0
        elif -5 <= true_count <= -1:
            true_count_bucket = 1
        elif -1 <= true_count <= 1:
            true_count_bucket = 2
        elif 2 <= true_count <= 5:
            true_count_bucket = 3
        elif true_count > 5:
            true_count_bucket = 4
        
        player_total_bucket = 0
        if player_total < 11:
            player_total_bucket = 0
        elif player_total < 15:
            player_total_bucket = 1
        else:
            player_total_bucket = 2
        
        return (player_total_bucket, dealer_total, usable_ace, true_count_bucket, action)
    
    def q_update(superState, action, reward, nextState, running_count):
        action = actions.index(action)
        running_count, true_count, decks_remaining = count_cards(running_count, nextState)
        statekey = find_key(superState, action)
        if nextState.hand_over:
            q_vals[statekey] += (alpha_vals[statekey] * (reward - q_vals[statekey]))
        else:
            next_player_score = nextState.player_score()
            nextSuperState = (true_count, next_player_score, check_ace(nextState), nextState.dealer_score())
            next_action = get_action(nextState) 
            next_action = actions.index(next_action)
            next_statekey = find_key(nextSuperState, next_action)
            td_target = reward + DISCOUNT_FACTOR * q_vals[next_statekey]
            td_error = td_target - q_vals[statekey]
            q_vals[statekey] += (alpha_vals[statekey] * td_error)
        alpha_vals[statekey] *= 0.999
    
    def calc_true_count(state):
        running_count = 0
        if state.deck.size() == 52*(state.shoe_size):
            return 0
        
        for card in state.deck.cards_played:
            if card.rank() == 1:
                running_count -= 1
            elif 2 <= card.rank() <= 6:
                running_count += 1
            elif 10 <= card.rank() <= 13:
                running_count -= 1

        true_count = running_count/(state.deck.size()/52)
        return true_count

    def get_optimal_action(state):
        true_count = calc_true_count(state)
        player_score = state.player_score()
        if player_score >= 21:
            player_score = 0
        superState = (true_count, player_score, check_ace(state), state.dealer_score())
        maxQ = float('-inf')
        maxAction = None
        if state.hand_over:
            for action in range(len(postflop_actions), len(actions)):
                Q_val = q_vals[find_key(superState, action)]
                if Q_val > maxQ:
                    maxQ = Q_val
                    maxAction = action
        else:
            for action in range(len(postflop_actions)):
                Q_val = q_vals[find_key(superState, action)]
                if Q_val > maxQ:
                    maxQ = Q_val
                    maxAction = action
        return actions[maxAction]

    postflop_actions = game.get_postflop_actions()
    betting_actions = game.bet_sizes
    actions = postflop_actions + betting_actions
    actions = tuple(actions)
    q_vals = {}
    alpha_vals = {}
    for action in range(len(actions)):
        for player in range(3): #hand_total
            for dealer in range(12): #dealer_total
                for true_count in range(5):
                    for ace in range(2):
                        q_vals[(player,dealer,ace,true_count,action)] = 0
                        alpha_vals[(player,dealer,ace,true_count,action)] = LEARNING_RATE

    end_time = time.time() + time_limit
    epsilon = EPSILON_START
    intial_state = game.initial_state()
    while time.time() < end_time:
        tmp = copy.deepcopy(intial_state)
        game.shuffle()
        game.new_shoe()
        running_count = 0
        true_count = 0
        decks_remaining = game.shoe_size * 6
        while tmp.deck.size() > (game.shoe_size*52)/pen:
            action = get_action(tmp)
            tmp = tmp.successor(action) # place bet and cards are dealt
            player_total = 15 if tmp.player_score() > 14 else tmp.player_score()
            dealer_total = tmp.dealer_score()
            running_count, true_count, decks_remaining = count_cards(running_count, tmp)
            usable_ace = check_ace(tmp)
            superState = (true_count, player_total, usable_ace, dealer_total)
            reward = 0
            while not tmp.hand_over:
                action = get_action(tmp) # postflop action (hit stand or double)
                tmp = tmp.successor(action)
                reward += tmp.payoff()
                q_update(superState, action, reward, tmp, running_count)
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    return get_optimal_action