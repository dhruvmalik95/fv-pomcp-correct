from robot import *
from rocksamplegame import *
from humanPolicy import *
from humannode import *
from root import *
from robotnode import *
from rocksamplepomcp import *
import math
import pickle

big_l = []
for _ in range(0, 20):
	initial_state = (0,0)
	rock_vector = [((2,1),0), ((1,2),1)]
	theta_set = [[1,0],[0.3,0.8]]
	game = Rocksample_Game(3, 3, 1, 1, initial_state, rock_vector, theta_set, 0.95)

	all_states = game.getAllStates()
	belief = []

	x = [initial_state, tuple(["no", "no"])]
	belief.append((x, 0))
	belief.append((x, 1))
	#belief.append((x, 2))
	print(belief)

	initial_history = Root(game, belief, 0)

	#make sure to change exploration accordingly - also what should the epsilon value be?
	epsilon = math.pow(0.95, 2)


#KEEP THESE PARAMETERS FOR NOW!!
	solver = Rocksample_POMCP_Solver(0.95, epsilon, 600000, initial_history, game, 500, 5)
	print(_)
	solver.search()
	data = solver.data
	l = []
	i = 3
	while i <= 5.775:
		l.append(data[round(10^i) - 1000])
		i = i + 0.13875
	big_l.append(l)	

f = open('data-pomcp.txt', 'w')
f.write(str(data))
print("_____________________")

"""
Things to keep in mind:
1. Make sure to change epsilon appropriately.
2. The game file has that weird shit about leaving the same state when the human and robot have the same
   action. Not sure if this matters or not? Maybe depends on epsilon?
3. Exploration should be >= 300 for >= million, maybe just a wee bit less for 10000.
4. For the Rational Function: I divide by 3. This is a cluge fix, make it like dependent on number of
   iterations...for >= 1 million this should be <= 1.
5. For the Rational Function: It's giving me a divide by zero error...this shouldn't happen, the visited
   should already be incremented.
"""
