import time, random, copy, blackjack
LEARNING_RATE = 0.25
DISCOUNT_FACTOR = 0.99
EPSILON = 0.15

def qlearn_policy(game, time_limit):
    def get_action(state):
        if random.random() < EPSILON:
            if state.player_hand == []:
                return random.randint(len(postflop_actions), len(actions))
            else:
                return random.randint(0, len(postflop_actions))
        else:
            return get_optimal_action(state)

    def get_optimal_action(state):
        pass

    postflop_actions = game.get_actions()
    betting_actions = game.bet_sizes
    actions = postflop_actions.extend(betting_actions)
    q_vals = {}
    alpha_vals = {}
    for action in range(len(actions)):
        for player in range(20): #hand_total
            for dealer in range(11): #dealer_total
                for ace in range(2):
                    q_vals[(player,dealer,ace, action)] = 0
                    alpha_vals[(player,dealer,ace, action)] = LEARNING_RATE

    end_time = time.time() + time_limit
    intial_state = game.initial_state()
    while time.time() < end_time:
        tmp = copy.deepcopy(intial_state)
        
        # state = (true_count, hand_total, usable_ace, dealer_total)
        game.shuffle()
        game.new_shoe()
        while not game.game_over():
            action = get_action()
            tmp.update_game(action)
            player_total = tmp.player_score()
            dealer_total = tmp.dealer_score()
            

    return get_optimal_action