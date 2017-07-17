class ActionNode:
	def __init__(self, game, value, visited):
		self.type = "action"
		self.game = game
		self.human_actions = self.game.getAllHumanActions()
		self.children = self.make_children()
		self.value = value
		self.visited = visited

	def make_children(self):
		children = []
		for action in self.human_actions:
			children.append("empty")

		return children

	def augmented_value(self, c):
		#test to make sure this division isnt just 0
		return self.value + c/self.visited

	def update_value(self, reward):
		val = self.value
		val = val + ((reward - val)/self.visited)
		self.value = val

	def update_visited(self):
		count = self.visited
		count = count + 1
		self.visited = count