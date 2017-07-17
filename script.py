from robot import *
from game import *
from humanPolicy import *
from humannode import *
from root import *
from robotnode import *
from pomcp import *
import math


def run(n_ingredients):
	num_theta = 2
	horizon = 0
	num_ingredients = n_ingredients

	"""
	CHANGE GAME FILE BASED ON SCRIPT!!
	"""

	robot_belief = [1/num_theta for i in range(num_theta)]

	if num_ingredients == 2:
		reward_set = [((0,3),0), ((2,2), 1)]
		initial_world_state = (0,0)
	elif num_ingredients == 3:
		reward_set = [((0,2,2),0), ((2,0,2), 1)]
		initial_world_state = (0,0,0)
	elif num_ingredients == 4:
		reward_set = [((0,2,2,0),0), ((2,0,2,0), 1)]
		initial_world_state = (0,0,0,0)
	elif num_ingredients == 5:
		reward_set = [((0,0,2,2,0),0), ((0,2,0,2,0), 1)]
		initial_world_state = (0,0,0,0,0)
	elif num_ingredients == 6:
		reward_set = [((0,0,2,2,0,0),0), ((0,2,0,2,0,0), 1)]
		initial_world_state = (0,0,0,0,0,0)
	elif num_ingredients == 7:
		reward_set = [((0,0,0,2,2,0,0),0), ((0,0,2,0,2,0,0), 1)]
		initial_world_state = (0,0,0,0,0,0,0)
	
	
	#initial_world_state = (0,0,0,0,0)
	human_behavior = "boltzmann"


	humanPolicy = HumanPolicy(num_actions = num_ingredients + 1, behavior = human_behavior)
	robot = Robot(robot_belief, num_actions = num_ingredients + 1)
	game = Game(robot, humanPolicy, initial_world_state, num_theta, num_ingredients, reward_set)

	if num_ingredients == 2:
		initial_history = Root(game, [((0,0),0), ((0,0),1)], 0)
	elif num_ingredients == 3:
		initial_history = Root(game, [((0,0,0),0), ((0,0,0),1)], 0)
	elif num_ingredients == 4:
		initial_history = Root(game, [((0,0,0,0),0), ((0,0,0,0),1)], 0)
	elif num_ingredients == 5:
		initial_history = Root(game, [((0,0,0,0,0),0), ((0,0,0,0,0),1)], 0)
	elif num_ingredients == 6:
		initial_history = Root(game, [((0,0,0,0,0,0),0), ((0,0,0,0,0,0),1)], 0)
	elif num_ingredients == 7:
		initial_history = Root(game, [((0,0,0,0,0,0,0),0), ((0,0,0,0,0,0,0),1)], 0)
	#make sure to change exploration accordingly - also what should the epsilon value be?
	epsilon = math.pow(0.95, 2)
	solver = POMCP_Solver(0.95, epsilon, 35000, initial_history, game, 10, 5)
	solver.search()
	return solver.data


big_l = []
for _ in range(2, 8):
#KEEP THESE PARAMETERS FOR NOW!!
	l = []
	for i in range(1,21):
		data = run(_)
		l.append(data[0])
	print(l)
	# l = []
	# for i in range(1,21):
	# 	l.append(data[round((math.e/1.62)**(i)) - 1])
	# print(l)
	big_l.append(l)
	print("_____________________")
f = open('data-fv-pomcp.txt', 'w')
f.write(str(big_l))
print(big_l)
print(len(big_l))
print(len(big_l[0]))

# for _ in range(0, 1):
# #KEEP THESE PARAMETERS FOR NOW!!
# 	solver = POMCP_Solver(0.95, epsilon, 35000, initial_history, game, 10, 5)
# 	solver.search()
# 	data = solver.data
# 	f = open('data-coor-pomcp.txt', 'w')
# 	f.write(str(data))
# 	print("_____________________")

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