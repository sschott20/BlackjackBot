# CPSC 474 Final Project
## Alex Shin, Alex Schott, Jinwoo Kim

### Project and Algorithms Overview
https://www.youtube.com/watch?v=vC7V89-iMBc&t=57s&ab_channel=AlexSchott


For this project we implemented monte carlo tree search, expectimax and q-learning. For basic agents to compare against, we have a few options, which are listed below. All agents use a dealer which hits until a 17, with the only actions being hit, stand, or double. We did not allow for splitting or insurance. 

Overall our best performance was with MCTs which simulates the entire remaining deck, and manages to win around $0.039 per hand on average (when bets are $1 - $10). This aligned with what we expected as our simplified version of blackjack had a low branching factor and MCTs allows for us to similuate the deck rather than having to deal with the exact probabilities. MCTs seem to be winning with a more aggressive betting spread and strategy, and is likely able to do significanly better than what our implementation observed. 

For Q-learning, we observed that it was able to learn a strategy that was able to win money, but it was not able to learn a strategy that was able to win money consistently. However, when giving the q-learning implementation a long period of time to train, it performs significantly better, which makes sense as it is able to run more episodes and converge to the optimal policy faster. We decreased the state space complexity with coarse coding, in order to converge to the optimal policy faster: we divided the true count into 5 buckets, and the player's hand into 3 buckets. 

For Expectimax, although we used a similar strategy to MCTs we were not able to get it to perform as well as MCTs. We believe this is due to the fact that we were not able to tune the parameters as well as we did for MCTs. Our implementation for expectimax calculates a 2d matrix that stores the odds of winning (ranging from -1 to 1). This matrix is calculated by maximizing the odds of its next two possible states, which are the resulting states from hitting or standing (did not include doubling). This matrix of odds is also used to calculate a heuristic which the agent uses to figure out how much it should bet each hand. Although, we were not able to get expectimax to perform as well as MCTs, we believe that with more time, we would be able to tune the parameters to get it to perform just as well if not better.


For each model down below, we are displaying the average profit earned over the total number of hands the agent played. That is, average profit = total money gained / lost over many shoes of play, divided by the total number of hands. We reshuffle once we have reached 80% deck penetration. 

always_hit: -0.657

always_stand: -0.179

dealer: -0.075

gambler: -0.116

MCTS with more deck simulation (count = 1000): 0.0391

Q-Learning (count = 100000, training time = 30 min): -0.0806

Expectimax with more deck simulation(count = 1000): -0.0646


### How to run test cases
If the executable is not already present, run `make` to compile and build the executable, then run `./TestBlackjack` to run our script. In this repository we have also added a shell script `./TestBlackjack.sh` which will perform the same actions as above. (Note: you may need to enable persmissions for the shell script by running `chmod +x ./TestBlackjack.sh`)


