.PHONY: TestBlackjack

TestBlackjack:
	echo "#!/bin/bash" > TestBlackjack
	echo "cat log" >> TestBlackjack
	echo "pypy3 test_blackjack.py --count 10000 --model always_stand --pen 6" >> TestBlackjack 
	echo "pypy3 test_blackjack.py --count 10000 --model always_hit --pen 6" >> TestBlackjack 
	echo "pypy3 test_blackjack.py --count 10000 --model hit_until --pen 6" >> TestBlackjack 
	echo "pypy3 test_blackjack.py --count 10000 --model gambler --pen 6" >> TestBlackjack 
	echo "pypy3 test_blackjack.py --count 10000 --model basic --pen 6" >> TestBlackjack 
	echo "pypy3 test_blackjack.py --count 1 --model mcts --pen 6 --time 0.1" >> TestBlackjack
	echo "pypy3 test_blackjack.py --count 1 --model mcts_no_tracking --pen 6 --time 0.1" >> TestBlackjack
	echo "pypy3 test_blackjack.py --count 1000 --model qlearn --pen 6 --time 20" >> TestBlackjack
	echo "pypy3 test_blackjack.py --count 100 --model xmax --pen 6" >> TestBlackjack
	chmod +x TestBlackjack