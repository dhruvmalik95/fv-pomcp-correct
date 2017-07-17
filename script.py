from robot import *
from game import *
from humanPolicy import *
from humannode import *
from root import *
from robotnode import *
from pomcp import *
import math

num_theta = 2
horizon = 0
num_ingredients = 3

robot_belief = [1/num_theta for i in range(num_theta)]
reward_set = [((0,2,2),0), ((2,0,2), 1)]
initial_world_state = (0,0,0)
#initial_world_state = (0,0,0,0,0)
human_behavior = "boltzmann"


humanPolicy = HumanPolicy(num_actions = num_ingredients + 1, behavior = human_behavior)
robot = Robot(robot_belief, num_actions = num_ingredients + 1)
game = Game(robot, humanPolicy, initial_world_state, num_theta, num_ingredients, reward_set)

initial_history = Root(game, [((0,0,0),0), ((0,0,0),1)], 0)

#make sure to change exploration accordingly - also what should the epsilon value be?
epsilon = math.pow(0.95, 2)

# print("Required Horizon: 4")
# print("Number Of Theta: 6")
# print("Number Of Ingredients: 5")

for _ in range(0, 1):
#KEEP THESE PARAMETERS FOR NOW!!
	solver = POMCP_Solver(0.95, epsilon, 30000, initial_history, game, 10, 5)
	solver.search()
	data = solver.data
	f = open('data-fv-pomcp.txt', 'w')
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