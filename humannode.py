class HumanNode:
	def __init__(self, game, reward):
		self.type = "human"
		self.game = game
		self.actions = self.game.getAllActions()
		self.children = self.make_children()
		self.theta_list = self.game.getAllTheta()
		# self.value_list = self.make_value_list(reward, theta)
		# self.visited_list = self.make_visited_list(theta)
		
		#check this:!!
		self.value = reward
		self.visited = 1

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

	# def optimal_action_factored(self, c):
	# 	for i in range(0, len(self.children)):
	# 		if self.children[i] == "empty":
	# 			return self.actions[i]

	# 	robot_action_Q_vals = []
	# 	for i in range(0, len(self.robot_actions)):
	# 		robot_action_Q_vals.append(self.robot_action_values[i]/self.robot_action_visited[i])
	# 	robot_action_opt = self.robot_actions[self.robot_actions.index(max(self.robot_actions))]

	# 	decision_rule_Q_vals = []
	# 	for i in range(0, len(self.decision_rules)):
	# 		decision_rule_Q_vals.append(self.decision_rule_values[i]/self.decision_rule_visited[i])
	# 	decision_rule_opt = self.decision_rules[self.decision_rules.index(max(self.decision_rules))]

	# 	#check the syntax for this shit
	# 	return (decision_rule_opt, robot_action_opt)


	def make_children(self):
		children = []
		for action in self.actions:
			children.append("empty")

		return children

	def optimal_action(self, c):
		for i in range(0, len(self.children)):
			if self.children[i] == "empty":
				return self.actions[i]

		values = []
		for i in range(0, len(self.children)):
			values.append(self.children[i].augmented_value(c))

		return self.actions[values.index(max(values))]

	def update_value(self, reward):
		val = self.value
		val = val + ((reward - val)/self.visited)
		self.value = val

	def update_visited(self):
		count = self.visited
		count = count + 1
		self.visited = count

	# def make_value_list(self, reward, theta):
	# 	#should this be the reward or gamma^depth*reward
	# 	l = [0 for _ in range(len(self.theta_list))]
	# 	l[self.theta_list[self.theta_list.index(theta)]] = reward
	# 	return l

	# def make_visited_list(self, theta):
	# 	l = [0 for _ in range(len(self.theta_list))]
	# 	l[self.theta_list[self.theta_list.index(theta)]] = 1
	# 	return l

	# def update_value(self, reward, theta):
	# 	theta_index = self.theta_list.index(theta)
	# 	val = self.value_list[theta_index]
	# 	val = val + ((reward - val)/self.visited_list[theta_index])
	# 	self.value_list[theta] = val

	# def update_visited(self, theta):
	# 	theta_index = self.theta_list.index(theta)
	# 	count = self.visited_list[theta_index]
	# 	count = count + 1
	# 	self.visited_list[theta_index] = count
