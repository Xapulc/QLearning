import numpy as np
from helpful_functions import puasson
from I2Point import I2Point


class Management(object):
    def __init__(self):
        self.arenda = 10
        self.peregonka = -2
        self.max_vehicles = 20
        self.max_peregonok = 5
        self.gamma = 0.9
        self.need_lambda1 = 3
        self.need_lambda2 = 4
        self.return_lambda1 = 3
        self.return_lambda2 = 2

        self.states = set()
        for i in range(self.max_vehicles):
            for j in range(self.max_vehicles):
                self.states.add(I2Point(i, j))

        self.values = {state: 0 for state in self.states}
        self.strategies = {state: None for state in self.states}
        self.actions = {state: {action for action in range(-self.max_peregonok, self.max_peregonok + 1)
                                if 0 <= state.x - action <= self.max_vehicles
                                and 0 <= state.y + action <= self.max_vehicles}
                        for state in self.states}
        # install distribution
        self.prob_action = {state: {action: 1 / len(self.actions[state]) for action in self.actions[state]}
                            for state in self.states}
        self.new_states = {state: self.states for state in self.states}

    def update_strategies(self):
        for state in self.states:
            value = max(self.prob_action[state].values())
            self.strategies[state] = np.random.choice({action for action in self.prob_action[state].keys()
                                                       if self.prob_action[state][action] == value})

    def probability(self, state, action, new_state):
        new_start_state = state + I2Point(-action, action)
        

    def strategies_estimate(self, delta0):
        delta = 2 * delta0
        while not delta < delta0:
            delta = 0
            for state in self.states:
                value = self.values[state]
                sm = 0
                for action in self.actions[state]:
                    for new_state in self.new_states[state]:
                        sm += self.prob_action[state][action] * self.probability(state, action, new_state) \
                              * (self.reward(state, action, new_state) + self.gamma * self.values[state])
                delta = max(delta, abs(value - self.values[state]))

    def iteration_strategies(self, delta0):
        pass
