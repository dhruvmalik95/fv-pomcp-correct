# Local Imports
from conditionalPlan import *

class Robot:
    """
    A robot agent.
    """
    def __init__(self, b, num_actions = 4):
        """
        Initializes an instance of the Robot class.

        Each action is a 3-tuple corresponding to (spinach, bread, tomatoes),
        where at most one of entries is 1 and the others are 0.
        e.g. (1,0,0): processSpinach()
        e.g. (0,0,0): wait()

        :param b: the robot's belief over theta. The list must contain
            non-negative entries and must sum to one.
        :param num_actions: the number of actions the robot may make.
        """
        self.b = b
        self.actions = self.generateActions(num_actions)

    def generateActions(self, num_actions):
        """
        Returns the list of actions that the robot can take given the number
        of actions she is allowed to make.

        :param num_actions:
        """
        actions = []
        for i in range(num_actions - 1):
            action = np.zeros(num_actions - 1)
            action[i] = 1
            actions.append(tuple(action))
        actions.append(tuple(np.zeros(num_actions - 1)))
        return actions

    def createInitialPlans(self, game):
        """
        Creates the initial set of plans i.e. plans at time T for the robot in
        the specified game.

        Since the reward is defined over states, all plans here will have the
        same alpha vector and hence we only need to define a single plan in the
        initial set.

        :param game: the game.
        """
        states = game.allStates

        trivial_plan = ConditionalPlan(game, None, None)
        initial_alpha = [0] * len(states)
        for state in states:
            initial_alpha[states.index(state)] = game.getReward(state)

        trivial_plan.alpha = initial_alpha

        trivial_map = {}
        for obs in game.allObservations:
            trivial_map[obs] = trivial_plan
        plans = [ConditionalPlan(game, action, trivial_map) for action in self.actions]
        #plans = [ConditionalPlan(game, self.actions[-1], trivial_map)]
        return plans

    def getBelief(self, game):
        """
        Returns the current belief vector over all states.

        :param game:
        """
        return self.getBeliefVector(game, game.world_state, self.b)

    def getBeliefVector(self, game, world_state, b):
        """
        Returns the belief states as a |S|-dimensional vector given a world
        state b and the belief that theta is 0.

        :param world_state: the current world state
        :param states: a Python list of states
        """
        belief = [0]*len(game.allStates)
        thetas = game.getAllTheta()
        for i in range(len(thetas)):
            belief[game.allStates.index((world_state, thetas[i]))] = b[i]
        return belief
