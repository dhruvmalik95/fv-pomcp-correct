import numpy as np
import math

class Root:
	def __init__(self, game, belief, visited):
		"""
		Initializes the root of the search tree.
		:param game: the game object that needs to be solved.
		:param belief: the initial belief of the coordinator.
		:param visited: the number of times the root has been visited
		"""
		self.type = "root"
		self.game = game
		self.actions = self.game.getAllActions()
		self.children = self.make_children()
		self.belief = belief
		self.visited = visited
		self.decision_rules = self.game.getAllDecisionRules()
		self.robot_actions = self.game.getAllRobotActions()
		self.decision_rule_values = self.make_decision_rule_values()
		self.robot_action_values = self.make_robot_action_values()
		self.robot_action_visited = self.make_robot_action_visits()
		self.decision_rule_visited = self.make_decision_rule_visits()

	def make_decision_rule_values(self):
		l = []
		for i in range(0, len(self.decision_rules)):
			l.append(0)
		return l

	def make_decision_rule_visits(self):
		l = []
		for i in range(0, len(self.decision_rules)):
			l.append(0)
		return l

	def make_robot_action_values(self):
		l = []
		for i in range(0, len(self.robot_actions)):
			l.append(0)
		return l

	def make_robot_action_visits(self):
		l = []
		for i in range(0, len(self.robot_actions)):
			l.append(0)
		return l

	def make_children(self):
		"""
		Makes the children action list of the root. Initializes each child to be the "empty"
		string since these children have not been visited yet.
		"""
		children = []
		for action in self.actions:
			children.append("empty")

		return children

	def optimal_action(self, c):
		"""
		Returns the optimal action to be taken (picks the one that hasn't been tried yet if there is one).
		:param c: the constant which affects how much exploration is needed.
		"""
		for i in range(0, len(self.children)):
			if self.children[i] == "empty":
				return self.actions[i]

		values = []
		for i in range(0, len(self.children)):
			values.append(self.children[i].augmented_value(c))

		return self.actions[values.index(max(values))]

	def optimal_action_factored(self, c):
		# for i in range(0, len(self.children)):
		# 	if self.children[i] == "empty":
		# 		return self.actions[i]

		robot_action_Q_vals = []
		for i in range(0, len(self.robot_actions)):
			robot_action_Q_vals.append(self.robot_action_values[i] + c/(self.robot_action_visited[i] + 1))
			#robot_action_Q_vals.append(self.robot_action_values[i]/self.robot_action_visited[i])
		robot_action_opt = self.robot_actions[robot_action_Q_vals.index(max(robot_action_Q_vals))]

		decision_rule_Q_vals = []
		for i in range(0, len(self.decision_rules)):
			decision_rule_Q_vals.append(self.decision_rule_values[i] + c/(self.decision_rule_visited[i] + 1))
			#decision_rule_Q_vals.append(self.decision_rule_values[i]/self.decision_rule_visited[i])
		decision_rule_opt = self.decision_rules[decision_rule_Q_vals.index(max(decision_rule_Q_vals))]

		#check the syntax for this shit
		return (decision_rule_opt, robot_action_opt)

	def sample_belief(self):
		"""
		Randomly selects a start state from the belief state.
		"""
		random_index = np.random.choice(range(0, len(self.belief)))
		return self.belief[random_index]

	def update_visited(self):
		"""
		Increment the number of times we have visited the root by 1.
		"""
		count = self.visited
		count = count + 1
		self.visited = count

	def update_value(self, reward):
		"""
		The root doesn't really have a value haha, this is just here to make the POMCP code work.
		"""
		return