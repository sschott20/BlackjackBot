from blackjack import *
import copy

def set_probs(deck, probs):
    # Reset probs
    for i in range(1, 11):
        probs[i] = 0
    
    # Calculate probs
    while deck.size() > 0:
        card = deck.deal(1)[0]
        if card.rank() >= 10:
            key = 10
        else:
            key = card.rank()
        probs[key] += 1
    
    for i in range(1, 11):
        probs[i] = probs[i]/52
   

def calculate_payoffs(state):
    def get_hit_payoff(dealer_rank, old_rank, new_rank, hit_payoff):
        total = old_rank + new_rank
        if total > 21:
            return -1
        else:
            return hit_payoff[dealer_rank][total]
        
    def get_stand_payoff(player_rank, old_rank, new_rank, stand_payoff):
        total = old_rank + new_rank
        if total > 21:
            return 1
        else:
            return stand_payoff[total][player_rank]
        

    probs = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0
    }
    # Calculate probabilities for deck
    tmp_state = copy.deepcopy(state)
    set_probs(tmp_state.deck, probs)

    # Calculate stand-payoff matrix using above probabilities
    stand_payoff = [[0 for _ in range(22)] for _ in range(22)]
    # Base cases:
    for i in range(17, 22):
        for j in range(22):
            if i > j:
                stand_payoff[i][j] = -1
            elif i < j:
                stand_payoff[i][j] = 1
            else:
                stand_payoff[i][j] = 0
    
    for i in range(16, -1, -1):
        for j in range(21, -1, -1):
            for c in range(1, 11):
                stand_payoff[i][j] += probs[c] * get_stand_payoff(j, i, c, stand_payoff)
    
    # Calculate hit-payoff matrix using above probabilities
    hit_payoff = [[0 for _ in range(22)] for _ in range(22)]
    action_matrix = [[0 for _ in range(22)] for _ in range(22)]
    # Base cases:
    hit_payoff[21][21] = 0
    hit_payoff[20][21] = 1
    hit_payoff[19][21] = 1
    hit_payoff[18][21] = 1
    hit_payoff[17][21] = 1
    for i in range(21, 16, -1):
        for j in range(20, -1, -1):
            hit_value = 0
            for c in range(1, 11):
                hit_value += probs[c] * get_hit_payoff(i, j, c, hit_payoff)
            stand_value = stand_payoff[i][j]
            if hit_value > stand_value:
                hit_payoff[i][j] = hit_value
                action_matrix[i][j] = "H"
            else:
                hit_payoff[i][j] = stand_value
                action_matrix[i][j] = "S"
    
    for i in range(16, -1, -1):
        for j in range(21, -1, -1):
            hit_value = 0
            for c in range(1, 11):
                hit_value += probs[c] * get_hit_payoff(i, j, c, hit_payoff)
            stand_value = stand_payoff[i][j]
            if hit_value > stand_value:
                hit_payoff[i][j] = hit_value
                action_matrix[i][j] = "H"
            else:
                hit_payoff[i][j] = stand_value
                action_matrix[i][j] = "S"
    
    return hit_payoff, stand_payoff, action_matrix, probs

def xmax_policy():
    def bet_heuristic(hit_payoff):
        total = 0
        divisor = 0
        for i in range(22):
            for j in range(22):
                total += hit_payoff[i][j]
                divisor += 1
        return total/divisor
                


    def best_move(state):
        hit_payoff, stand_payoff, action_matrix, probs = calculate_payoffs(state)
        actions = state.get_actions()
        # Figure out betting size
        if len(actions) == 3:
            heuristic = bet_heuristic(hit_payoff)
            if heuristic < 0:
                return 1
            elif heuristic > 0.02:
                return 7
            else:
                return 4
        # Figure out best move
        else:
            print(state)
            print(stand_payoff)
            print(action_matrix[16][21])
            input()
            return action_matrix[state.dealer_score()][state.player_score()]
    
    return best_move


