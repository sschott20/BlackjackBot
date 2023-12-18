import time, random, copy, blackjack
LEARNING_RATE = 0.25
DISCOUNT_FACTOR = 0.99
EPSILON = 0.15

def qlearn_policy(game, time_limit):
    def get_action(state):
        if random.random() < EPSILON:
            if len(state.player_hand) == 0 or state.hand_over:
                print('bet')
                return actions[random.randint(len(postflop_actions), len(actions)-1)]
            else:
                print('hit or stand')
                return actions[random.randint(0, len(postflop_actions)-1)]
        else:
            print('opt')
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
        decks_remaining = float(state.deck.size()/52)
        true_count = running_count/decks_remaining
        return running_count, true_count, decks_remaining
    
    def check_ace(state):
        for card in state.player_hand:
            if card.rank() == 1:
                return 1
        return 0
    
    def find_key(superState, action):
        true_count, player_total, usable_ace, dealer_total = superState
        bucket = 0
        if true_count < -5:
            bucket = 0
        elif -5 <= true_count <= -1:
            bucket = 1
        elif -1 <= true_count <= 1:
            bucket = 2
        elif 2 <= true_count <= 5:
            bucket = 3
        elif true_count > 5:
            bucket = 4
        
        return (player_total,dealer_total,usable_ace,bucket,action)
    
    def q_update(superState, action, reward, nextState, running_count):
        # need to identify the next state and the next action
        # dealers and players hands are now known
        # need to update running count
        action = actions.index(action)
        running_count, true_count, decks_remaining = count_cards(running_count, nextState)
        statekey = find_key(superState, action)
        if nextState.hand_over:
            q_vals[statekey] += (alpha_vals[statekey] * (reward - q_vals[statekey]))
        else:
            nextSuperState = (true_count, nextState.player_score(), check_ace(nextState), nextState.dealer_score())
            next_action = get_action(nextState) 
            next_action = actions.index(next_action)
            next_statekey = find_key(nextSuperState, next_action)
            td_target = reward + DISCOUNT_FACTOR * q_vals[next_statekey]
            td_error = td_target - q_vals[statekey]
            q_vals[statekey] += (alpha_vals[statekey] * td_error)
        alpha_vals[statekey] *= 0.99
    
    def calc_true_count(state):
        print(state.deck.cards_played)
        # deck = blackjack.Deck(range(1,14), ['S', 'H', 'D', 'C'], state.shoe_size)
        # print(deck._cards)
        # print(len(state.deck._cards))
        if state.deck.size() == 52*(state.shoe_size):
            return 0
        
        for card in state.deck.cards_played:
            running_count = 0
            if card.rank() == 1:
                running_count -= 1
            elif 2 <= card.rank() <= 6:
                running_count += 1
            elif 10 <= card.rank() <= 13:
                running_count -= 1
        
        # for card in state.deck._cards:
        #     pass
        #     # deck.remove(card)
        # running_count = 0
        # for card in deck:
        #     if card.rank() == 1:
        #         running_count -= 1
        #     elif 2 <= card.rank() <= 6:
        #         running_count += 1
        #     elif 10 <= card.rank() <= 13:
        #         running_count -= 1
        #     print(running_count)
        true_count = running_count/(state.deck.size()/52)
        print(true_count)
        return true_count

    def get_optimal_action(state):
        # need to calculate the true count from the state given
        true_count = calc_true_count(state)
        superState = (true_count, state.player_score(), check_ace(state), state.dealer_score())
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
    q_vals = {}
    alpha_vals = {}
    for action in range(len(actions)):
        for player in range(20): #hand_total
            for dealer in range(11): #dealer_total
                for true_count in range(5):
                    for ace in range(2):
                        q_vals[(player,dealer,ace,true_count,action)] = 0
                        alpha_vals[(player,dealer,ace,true_count,action)] = LEARNING_RATE

    end_time = time.time() + time_limit
    intial_state = game.initial_state()
    while time.time() < end_time:
        tmp = copy.deepcopy(intial_state)
        # state = (true_count, hand_total, usable_ace, dealer_total)
        game.shuffle()
        game.new_shoe()
        running_count = 0
        true_count = 0
        decks_remaining = game.shoe_size * 6
        while not game.game_over():
            print(tmp)
            action = get_action(tmp)
            print(f"action: {action}")
            tmp.update_game(action) # place bet and cards are dealt
            print(tmp)
            player_total = tmp.player_score()
            dealer_total = tmp.dealer_score()
            running_count, true_count, decks_remaining = count_cards(running_count, tmp)
            usable_ace = check_ace(tmp)
            superState = (true_count, player_total, usable_ace, dealer_total)
            reward = 0
            while not tmp.hand_over:
                action = get_action(tmp) # postflop action (hit or stand)
                print(f"action: {action}")
                tmp.update_game(action)
                print(tmp)
                reward += tmp.payoff()
                q_update(superState, action, reward, tmp, running_count)
            print('hand over')

    return get_optimal_action