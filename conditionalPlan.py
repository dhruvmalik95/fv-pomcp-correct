import numpy as np

class ConditionalPlan:
    """
    A class representing a conditional plan, which is a mapping from actions
    and observations to other conditional plans.
    """
    def __init__(self, game, action, mapp):
        """
        Initializes an instance of a Conditional Plan (at time t).

        :param game: the game (POMDP) in which this plan is defined.
        :param action: the coordinator action to be taken at time t; this is a
            tuple containing a decision rule for the human and an action for
            the robot.
        :param mapp: a map from possible observations to conditional plans at
            time t-1.
        :param alpha: the alpha vector; the i^{th} entry of this vector
            corresponds to the value of the plan at (world_state, theta)_i.
        """
        self.game = game
        self.action = action
        self.mapp = mapp
        self.alpha = None
        self.has_received_reward = False

    def getAlpha(self):
        """
        Returns the alpha vector of this plan if it has already been evaluated.
        If not, computes the alpha vector and then returns it.
        """
        if self.alpha:
            return self.alpha
        states = self.game.allStates
        observations = self.game.allObservations

        robot_action = self.action[1]
        alpha = [None]*len(states)

        for initial_state in states:
            if self.game.getReward(initial_state) == 1: # SPECIFIC TO CHEFWORLD GAME
                alpha[states.index(initial_state)] = 1 # SPECIFIC TO CHEFWORLD GAME
                continue # SPECIFIC TO CHEFWORLD GAME
            reward = 0 # SPECIFIC TO CHEFWORLD GAME - UNCOMMENT LINE BELOW TO GENERALIZE

            #reward = self.game.getReward(initial_state)
            sum_over_actions = 0
            for human_action in observations:
                P_human_action = self.game.human_policy.probAction(human_action, initial_state, self)
                if P_human_action == 0:
                    continue
                sum_over_states = 0
                for next_state in states:
                    T = self.game.transition(initial_state, self, human_action, next_state)
                    if T == 0:
                        continue
                    next_plan = self.mapp[human_action]
                    try:
                        value = next_plan.getAlpha()[states.index(next_state)]
                    except ValueError:
                        value = -100
                    sum_over_states += (T * value)
                sum_over_actions += (P_human_action * sum_over_states)
            alpha[states.index(initial_state)] = reward + self.game.gamma * sum_over_actions
        self.alpha = alpha
        return alpha

    def computeQ(self, state, prnt=False):
        """
        Returns a Python list containing the Q-value for taking any human
        action, given that the robot executes this conditional plan, at some
        state.

        :param state: the current state.
        :param theta: the human's true reward parameter.
        """
        observations = self.game.allObservations
        Q_values = []
        for human_action in observations:
            next_state = self.game.getNextState(state, self.action, human_action)
            if next_state[0] == ():
                print(next_state)
            try:
                value = self.mapp[human_action].alpha[self.game.allStates.index(next_state)]
            except ValueError:
                value = -100
            Q_values.append(value)
        return Q_values


    def evaluateBelief(self, belief):
        """
        Returns the value of a plan given a belief.

        :param belief: a list of length len(states)
        """
        return np.array(self.getAlpha()).dot(np.array(belief))
