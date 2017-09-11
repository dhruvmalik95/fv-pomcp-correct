import numpy as np
import math

from humannode import *
from robotnode import *
from timeit import default_timer as timer

class POMCP_Solver:
	def __init__(self, gamma, epsilon, timer, history, game, c, beta):
		"""
		creates a instance of a POMCP_Solver.
		:param gamma: this is the discount factor
		:param epsilon: this is the tolerance factor at which the rollout can be stopped
		:param timer: this is how long the search function is called
		:param history: this is the history from which the search function will be called
		:param game: the game that we pass in
		:param c: the constant which affects how much exploration vs. exploitation we want
		:param beta: the constant which measures human rationality
		"""
		self.gamma = gamma
		self.epsilon = epsilon
		self.timer = timer
		self.history = history
		self.game = game
		self.c = c
		self.beta = beta
		self.actions = self.game.getAllActions()
		print(len(self.actions))
		self.human_actions = self.game.getAllHumanActions()
		self.theta_list = self.game.getAllTheta()
		self.decision_rules = self.game.getAllDecisionRules()
		self.robot_actions = self.game.getAllRobotActions()
		self.data = []

	def search(self):
		"""
		Begins the Search function as described in Silver at al. Samples start states 
		self.timer many times. Prints optimal action.
		"""
		start_0 = timer()
		start = start_0
		for _ in range(0, self.timer):
			print(_)
			if _ % 100000 == 0:
				print(_)
			sample_state = self.history.sample_belief()
			self.simulate(sample_state, self.history, 0)
			
			# t = timer()
			# if t - start > 0.05 and _ > 64:
			# 	optimal_action = self.history.optimal_action(0)
			# 	optimal_child = self.history.children[self.actions.index(optimal_action)]
			# 	self.data.append((t-start_0, optimal_child.value))
			# 	start = t

			# if timer() - start_0 > 4*60:
			# 	return

			if _ > 999 and _ % 500 == 0:
				optimal_action = self.history.optimal_action_factored(0)
				optimal_child = self.history.children[self.actions.index(optimal_action)]
				self.data.append((_,optimal_child.value))
			# if _ > 4:
				# print(self.history.children[self.actions.index((0,0,1))].value)
				# print(self.history.children[self.actions.index((0,0,1))].visited)

		optimal_action = self.history.optimal_action_factored(0)
		optimal_child = self.history.children[self.actions.index(optimal_action)]

		print((optimal_action, optimal_child.value))
		# print(optimal_child.visited)
		# print(self.history.decision_rule_visited)

		l = []
		for child in self.history.children:
			if child != "empty":
				l.append(child.value)
		print(l)
		#print(optimal_child.visited)
		
		# # #THIS TEST CASE NOW WORKS!!
		#for action in self.history.children:

		# # #THIS TEST CASE DOES NOT - also test visited of right below optimal child - wait it does now??!
		# for action in optimal_child.children[0].children:
		# 	print(action.visited)
		# 	t = 0
		# 	for child in action.children:
		# 		for i in range(0, len(self.theta_list)):
		# 			t = t + child.visited_list[i]
		# 	print(t)
		# 	print(" ")
		# 	t = 0
		return self.data

	def random_sample(self, list_to_sample):
		random_index = np.random.choice(range(0, len(list_to_sample)))
		return list_to_sample[random_index]

	def rollout_helper(self, state, coordinator_action, history, depth):
		new_human_action = self.game.getHumanAction(state, coordinator_action)
		value = self.rollout(state, coordinator_action, depth)

		#check this.
		new_coordinator_action_child = ActionNode(self.game, value, 1)
		new_human_obs_child = HumanNode(self.game, value)
		new_coordinator_action_child.children[self.human_actions.index(new_human_action)] = new_human_obs_child
		history.children[self.actions.index(coordinator_action)] = new_coordinator_action_child

		#these should be here.
		history.update_visited()
		history.update_value(value)
		decision_rule = coordinator_action[0]
		robot_action = coordinator_action[1]

		history.decision_rule_visited[self.decision_rules.index(decision_rule)] += 1
		history.robot_action_visited[self.robot_actions.index(robot_action)] += 1

		history.decision_rule_values[self.decision_rules.index(decision_rule)] += (1 - history.decision_rule_values[self.decision_rules.index(decision_rule)])/history.decision_rule_visited[self.decision_rules.index(decision_rule)]
		history.robot_action_values[self.robot_actions.index(robot_action)] += (1 - history.robot_action_values[self.robot_actions.index(robot_action)])/history.robot_action_visited[self.robot_actions.index(robot_action)]
		

		return value

	def rollout(self, state, coordinator_action, depth):
		if math.pow(self.gamma, depth) < self.epsilon:
			return 0

		if self.game.getReward(state):
			return 1

		next_state = self.game.getNextState(state, coordinator_action)
		next_coordinator_action = self.random_sample(self.actions)

		#this should multiply the gamma here right?
		return self.gamma*self.rollout(next_state, next_coordinator_action, depth + 1)

	def simulate(self, state, history, depth):
		if math.pow(self.gamma, depth) < self.epsilon:
			return 0

		if self.game.getReward(state):
			history.update_visited()
			history.update_value(1)
			return 1


		optimal_action = history.optimal_action_factored(self.c)
		# optimal_action = history.optimal_action(self.c)
		# if optimal_action == ([(0, (0.0, 1.0, 0.0)), (1, (1.0, 0.0, 0.0))], (0.0, 0.0, 1.0)):
		# 	print("now")
		
		if history.children[self.actions.index(optimal_action)] == "empty":
			rollout_value = self.rollout_helper(state, optimal_action, history, depth)
			#should this be the reward or gamma^depth*reward
			return rollout_value

		# if self.behavior == "boltzmann":
		# 	next_state, human_action = self.sampleBoltzmann(state, optimal_action, history)
		# elif self.behavior == "rational":
		# 	next_state, human_action = self.sampleRational(state, optimal_action, history)
		# else:
		# 	print("wrong behavior input")

		human_action = self.game.getHumanAction(state, optimal_action)
		next_state = self.game.getNextState(state, optimal_action)

		next_history = history.children[self.actions.index(optimal_action)].children[self.human_actions.index(human_action)]
		if next_history == "empty":
			new_human_obs_child = new_human_obs_child = HumanNode(self.game, 0)
			#new_human_obs_child.visited_list[self.theta_list.index(state[1])] -= 1
			new_human_obs_child.visited -= 1
			history.children[self.actions.index(optimal_action)].children[self.human_actions.index(human_action)] = new_human_obs_child
			next_history = history.children[self.actions.index(optimal_action)].children[self.human_actions.index(human_action)]

		R = self.gamma*self.simulate(next_state, next_history, depth + 1)

		history.children[self.actions.index(optimal_action)].update_visited()
		history.children[self.actions.index(optimal_action)].update_value(R)

		#I THINK this should be history and not next_history. Otherwise overcount during rollouts.
		history.update_visited()
		history.update_value(R)

		decision_rule = optimal_action[0]
		robot_action = optimal_action[1]

		history.decision_rule_visited[self.decision_rules.index(decision_rule)] += 1
		history.robot_action_visited[self.robot_actions.index(robot_action)] += 1

		history.decision_rule_values[self.decision_rules.index(decision_rule)] += (R - history.decision_rule_values[self.decision_rules.index(decision_rule)])/history.decision_rule_visited[self.decision_rules.index(decision_rule)]
		history.robot_action_values[self.robot_actions.index(robot_action)] += (R - history.robot_action_values[self.robot_actions.index(robot_action)])/history.robot_action_visited[self.robot_actions.index(robot_action)]
		

		return R

	# def sampleBoltzmann(self, state, robot_action, history):
	# 	theta = state[1]
	# 	theta_index = self.theta_list.index(theta)
	# 	qValues = []
	# 	list_of_probabilities = []
		
	# 	for child in history.children[self.actions.index(robot_action)].children:
	# 		#add exploration bonus for 0 times human action for that theta HERE
	# 		if child == "empty":
	# 			qValues.append(1)
	# 			#print("x")
	# 		else:
	# 			qValues.append(child.value_list[theta_index])

	# 	#print(qValues)
	# 	qValues = np.array(qValues)
	# 	expQ_values = np.exp(self.beta * qValues)
	# 	total = sum(expQ_values)
		
	# 	for x in list(expQ_values):
	# 		list_of_probabilities.append(x / total)

	# 	random_index = np.random.choice(range(0, len(self.observations)), p = list_of_probabilities)
	# 	random_human_action = self.observations[random_index]
	# 	next_state = self.game.getNextState(state, robot_action, random_human_action)

	# 	return next_state, random_human_action

	# def sampleRational(self, state, robot_action, history):
	# 	theta = state[1]
	# 	theta_index = self.theta_list.index(theta)
	# 	qValues = []
		
	# 	for child in history.children[self.actions.index(robot_action)].children:
	# 		#add exploration bonus for 0 times human action for that theta HERE
	# 		if child == "empty":
	# 			child_index = history.children[self.actions.index(robot_action)].children.index(child)
	# 			next_human_action = self.observations[child_index]
	# 			next_state = self.game.getNextState(state, robot_action, next_human_action)
	# 			return next_state, next_human_action
	# 			#print("x")
	# 		else:
	# 			qValues.append(child.value_list[theta_index] + self.c/(3*child.visited_list[theta_index] + 1))

	# 	best_index = qValues.index(max(qValues))
	# 	next_human_action = self.observations[best_index]
	# 	next_state = self.game.getNextState(state, robot_action, next_human_action)
	# 	return next_state, next_human_action

