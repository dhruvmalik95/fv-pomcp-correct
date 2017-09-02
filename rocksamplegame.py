import itertools

class Rocksample_Game:

    def __init__(self, M, N, robot_action_length, human_action_length, initial_position, rock_vector, theta_set, gamma = 0.95):
        """
        Initializes an instance of the CIRL Rocksample game.
        
        :param M: the x distance of the grid.
        :param N: the y distance of the grid.
        :param robot_action_length: the number of time steps the robot can act on its own.
        :param human_action_length: the number of time steps the human can act on its own.
        :param initial_position: the starting position coordinate of the game.
        :param rock_vector: a vector containing a tuple for each rock - the tuple contains the position and type of the rock.
        :param theta_set: the set of theta_vectors over which the robot has uncertainty. A theta vector has an entry for the reward corresponding to each type of rock.
        :param gamma: the discount factor.
        """
        
        self.M = M
        self.N = N
        self.robot_action_length = robot_action_length
        self.human_action_length = human_action_length
        self.current_position = (initial_position, tuple(["no"] * len(rock_vector)))
        self.rock_vector = rock_vector
        self.theta_set = theta_set
        self.gamma = gamma

        self.grid = self.createGrid(M, N, initial_position)
        print(self.current_position)

    def createGrid(self, M, N, initial_position):
        """
        :param M: x distance of grid
        :param N: y distance of grid
        :param initial_position: a pair of indices in the grid

        Returns an M by N two dimensional array of 0's (and a 1 representing the inital position).
        """
        grid = [[0 for y in range(N)] for x in range(M)]
        grid[initial_position[0]][initial_position[1]] = 1
        return grid

    def getAllWorldStates(self):
        """
        Returns an array of all possible current locations.
        """
        # all possible locations
        array = []
        for x in range(self.M):
            for y in range(self.N):
                array.append((x,y))
        # all possible combinations of "yes"/"no" as to whether the rock has been sampled
        num_rocks = len(self.rock_vector)
        is_sampled = list(itertools.product(*[["no", "yes"] for i in range(num_rocks)]))
        # all states
        return list(itertools.product(array, is_sampled))
    
    def getAllTheta(self):
        """
        Returns all possible values of theta as a Python list.
        """
        return range(len(self.theta_set))
    
    def getAllStates(self):
        """
        Returns all possible states in the POMDP game as a Python list.
        """
        return list(itertools.product(self.getAllWorldStates(), self.getAllTheta()))

    # def generateActionsLengthK(self, k):
    #     """
    #     Generates all actions with length <= k.
    #
    #     :param k: the maximum length of action desired.
    #     :return: a list of tuples containing all actions with length <= k
    #     """
    #     actions = list(itertools.product(range(-k, k+1), range(-k, k+1)))
    #     actions = [tuple(action) for action in actions if abs(action[0]) + abs(action[1]) <= k]
    #     actions.append("sample")
    #     return actions

    def getHumanAction(self, state, coordinator_action):
        """
        Returns the human action to be taken given a state and decision_rule.
        :param state: used to get the theta as input to decision_rule
        :param decision_rule: the decision rule needed to get the output human action
        """
        decision_rule = coordinator_action[0]
        theta = state[1]
        for item in decision_rule:
            if item[0] == theta:
                return item[1]

    def getAllActions(self):
        """
        Returns all possible joint actions of the coordinator.
        """
        decision_rules = self.getAllDecisionRules()
        return list(itertools.product(decision_rules, self.getAllRobotActions()))

    def getAllDecisionRules(self):
        """
        Returns all possible decision rules that the coordinator could pick.
        """

        #check this shit lol?
        thetas = self.getAllTheta()
        human_actions = self.getAllHumanActions()
        return [list(zip(thetas, item)) for item in itertools.product(human_actions, repeat=len(thetas))]

    def getAllRobotActions(self):
        """
        Returns an array of all possible robot actions.
        """
        # creating all actions of length <= k
        actions = [(1,0), (-1,0), (0,1), (0,-1), (0,0), "sample"]
        if self.robot_action_length == 1:
            actions = [[(1,0)], [(-1,0)], [(0,1)], [(0,-1)], [(0,0)], ["sample"]]
        else:
            actions = list(itertools.product(*[actions for _ in range(self.robot_action_length)]))
            actions = [list(action) for action in actions]
        return actions

    def getAllHumanActions(self):
        """
        Returns an array of all possible human actions.
        """
        actions = [(1,0), (-1,0), (0,1), (0,-1), (0,0), "sample"]
        if self.human_action_length == 1:
            actions = [[(1,0)], [(-1,0)], [(0,1)], [(0,-1)], [(0,0)], ["sample"]]
        else:
            actions = list(itertools.product(*[actions for _ in range(self.human_action_length)]))
            actions = [list(action) for action in actions]
        return actions


    def getReward(self, state, coordinator_action):
        robot_action = coordinator_action[1]
        human_action = self.getHumanAction(state, coordinator_action)

        actions = robot_action[:]
        actions.extend(human_action[:])
        total_reward = 0
        for a in actions:
            if a == "sample":
                position = state[0][0]
                rock_sampled_information = state[0][1]
                theta = state[1]
                for rock in self.rock_vector:
                    rock_position = rock[0]
                    rock_type = rock[1]
                    if rock_position[0] == position[0] and rock_position[1] == position[1]:
                        if rock_sampled_information[rock_type] == "no":
                            # print(rock_type)
                            # print("f")
                            total_reward += self.theta_set[theta][rock_type]
            state = self.getNextStateOther(state, [a], [])
        return total_reward

    # def getReward(self, state, robot_action, human_action):
    #     """
    #     :param state: the augmented state.
    #
    #     Returns the reward for taking some pair of actions in a given state.
    #     """
    #     # If either agent chooses "sample"
    #     if robot_action == "sample" or human_action == "sample":
    #         position = state[0][0]
    #         rock_sampled_information = state[0][1]
    #         theta = state[1]
    #         for rock in self.rock_vector:
    #             rock_position = rock[0]
    #             rock_type = rock[1]
    #             if rock_position[0] == position[0] and rock_position[1] == position[1]:
    #                 if rock_sampled_information[rock_type] == "no":
    #                     #print(rock_type)
    #                     #print("f")
    #                     return self.theta_set[theta][rock_type]
    #         return 0
    #     # If the robot moves out of the board
    #     # state == next_state means that the robot was moved out of the board since we know that the human's action
    #     # is not sample and so, the robot must have moved
    #     next_state = self.getNextState(state, robot_action, human_action)
    #     if state == next_state:
    #         #print("shit")
    #         return 0
    #
    #     return 0

    def getNextStateOther(self, current_state, robot_action, human_action):
        actions = list(robot_action[:])
        actions.extend(human_action[:])
        for action in actions:
            x, y = current_state[0][0]
            old_x = x
            old_y = y
            rock_is_sampled_values = list(current_state[0][1])
            theta = current_state[1]

            if action == "sample":
                for rock in self.rock_vector:
                    if rock[0][0] == x and rock[0][1] == y:
                        # print(rock_is_sampled_values)
                        rock_is_sampled_values[rock[1]] = "yes"
                        # print(rock_is_sampled_values)
                current_state = ([(x, y), tuple(rock_is_sampled_values)], theta)
                continue
            else:
                x = x + action[0]
                y = y + action[1]
            if x >= self.M or x < 0 or y >= self.N or y < 0:  # if out of board
                current_state = ([(old_x, old_y), tuple(rock_is_sampled_values)], theta)
            else:
                current_state = ([(x, y), tuple(rock_is_sampled_values)], theta)
        return current_state

    def getNextState(self, current_state, coordinator_action):
        robot_action = coordinator_action[1]
        human_action = self.getHumanAction(current_state, coordinator_action)

        actions = list(robot_action[:])
        actions.extend(human_action[:])
        for action in actions:
            x, y = current_state[0][0]
            old_x = x
            old_y = y
            rock_is_sampled_values = list(current_state[0][1])
            theta = current_state[1]

            if action == "sample":
                for rock in self.rock_vector:
                    if rock[0][0] == x and rock[0][1] == y:
                        # print(rock_is_sampled_values)
                        rock_is_sampled_values[rock[1]] = "yes"
                        # print(rock_is_sampled_values)
                current_state = ([(x, y), tuple(rock_is_sampled_values)], theta)
                continue
            else:
                x = x + action[0]
                y = y + action[1]
            if x >= self.M or x < 0 or y >= self.N or y < 0:  # if out of board
                current_state = ([(old_x, old_y), tuple(rock_is_sampled_values)], theta)
            else:
                current_state = ([(x, y), tuple(rock_is_sampled_values)], theta)
        return current_state

    # def getNextState(self, current_state, robot_action, human_action):
    #     x, y = current_state[0][0]
    #     old_x = x
    #     old_y = y
    #     rock_is_sampled_values = list(current_state[0][1])
    #     theta = current_state[1]
    #
    #     # changing value of rock to sampled - CAN PROBABLY BE REPLACED WITH A TRY/EXCEPT BLOCK
    #     if robot_action == "sample" or human_action == "sample":
    #         for rock in self.rock_vector:
    #             if rock[0][0] == x and rock[0][1] == y:
    #                 #print(rock_is_sampled_values)
    #                 rock_is_sampled_values[rock[1]] = "yes"
    #                 #print(rock_is_sampled_values)
    #
    #     if robot_action == "sample" and human_action == "sample":
    #         return ([(x, y), tuple(rock_is_sampled_values)], theta)
    #     elif robot_action == "sample":
    #         x = x + human_action[0]
    #         y = y + human_action[1]
    #     elif human_action == "sample":
    #         x = x + robot_action[0]
    #         y = y + robot_action[1]
    #     else:
    #         x = x + robot_action[0] + human_action[0]
    #         y = y + robot_action[1] + human_action[1]
    #
    #     if x >= self.M or x < 0 or y >= self.N or y < 0: # if out of board
    #         return ([(old_x, old_y), tuple(rock_is_sampled_values)], theta)
    #     else:
    #         return ([(x, y), tuple(rock_is_sampled_values)], theta)
    #

    def transition(self, initial_state, robot_plan, human_action, final_state):
        return

