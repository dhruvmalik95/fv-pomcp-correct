import numpy as np
from operator import *

class HumanPolicy:
    """
    The policy that the human follows.
    """
    def __init__(self, num_actions = 4, behavior = "pedagogic-botlzmann", beta = 5):
        """
        Creates an instance of the HumanPolicy object.

        :param behavior: the behaviour of the human. Current options are
            "irl-rational", "irl-boltzmann", "pedagogic-rational", and
            "pedagogic-boltzmann".
        :param beta: the tuning parameter for the human's level of Boltzmann
            rationality. Only required if the human's behavior is boltzmann.
        :param num_actions: the number of actions the human may make.
        :param irl_q_value_function: the Q-value function for the human in the
            standard IRL case.
        """
        self.behavior = behavior
        self.beta = beta
        self.actions = self.generateActions(num_actions)
        self.irl_q_value_function = None

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

    def waitAction(self):
        """
        Returns the wait action.
        """
        return self.actions[-1]

    def probAction(self, human_action, initial_state, robot_plan):
        """
        Returns the probability of picking some action from initial_state given
        the robot's conditional plan.

        :param human_action:
        :param initial_state:
        :param robot_plan:
        """
        if self.behavior == "irl-rational":
            return self.probActionIrlRational(human_action, initial_state, robot_plan)
        elif self.behavior == "irl-boltzmann":
            return self.probActionIrlBoltzmann(human_action, initial_state, robot_plan)
        elif self.behavior == "pedagogic-rational":
            return self.probActionPedagogicRational(human_action, initial_state, robot_plan)
        elif self.behavior == "pedagogic-boltzmann":
            return self.probActionPedagogicBoltzmann(human_action, initial_state, robot_plan)

    def probActionPedagogicRational(self, human_action, initial_state, robot_plan):
        """
        Returns the probability of picking some action from initial_state given
        the robot's action if the human behaves pedagogically and rationally.

        :param human_action:
        :param initial_state:
        :param robot_plan:
        """
        qValues = robot_plan.computeQ(initial_state)
        optimal_index = np.argmax(qValues)
        optimal_action = self.actions[optimal_index]
        return (human_action == optimal_action) * 1

    def probActionPedagogicBoltzmann(self, human_action, initial_state, robot_plan):
        """
        Returns the probability of picking some action from initial_state given
        if the human behaves pedagogically and Boltzmann rationally.

        :param human_action:
        :param initial_state:
        :param robot_plan:
        """
        qValues = np.array(robot_plan.computeQ(initial_state))
        expQ_values = list(np.exp(self.beta * qValues))
        expQ_human_action = expQ_values[self.actions.index(human_action)]
        return expQ_human_action/sum(expQ_values)

    def probActionIrlRational(self, human_action, initial_state, robot_plan):
        """
        Returns the probability of picking some action from initial_state given
        if the human behaves rationally, independently of the robot.

        :param human_action:
        :param initial_state:
        :param robot_plan:
        """
        robot_action = robot_plan.action
        qValues = []
        for h_action in self.actions:
            qValues.append(self.irl_q_value_function[initial_state, robot_action, h_action])
        optimal_index = np.argmax(qValues)
        optimal_action = self.actions[optimal_index]
        return (human_action == optimal_action) * 1

    def probActionIrlBoltzmann(self, human_action, initial_state, robot_plan):
        """
        Returns the probability of picking some action from initial_state given
        if the human behaves Boltzmann rationally, independently of the robot.

        :param human_action:
        :param initial_state:
        :param robot_plan:
        """
        robot_action = robot_plan.action
        expQ_human_action = np.exp(self.beta * self.irl_q_value_function[(initial_state, robot_action, human_action)])
        expQ_values = []
        for h_action in self.actions:
            expQ_values.append(np.exp(self.beta * self.irl_q_value_function[(initial_state, robot_action, h_action)]))
        return expQ_human_action/sum(expQ_values)
