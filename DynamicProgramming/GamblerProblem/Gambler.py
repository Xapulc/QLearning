import matplotlib.pyplot as plt


class Gambler(object):
    def __init__(self, limit, p=0.5):
        self.p = p
        self.gamma = 1

        self.limit = limit
        self.states = {i for i in range(1, self.limit)}
        self.terminal_states = {0, self.limit}
        self.values = {state: 0 for state in self.states.union(self.terminal_states)}
        self.policy = {state: None for state in self.states}

    def actions(self, state):
        return {action for action in range(1, min(state, self.limit - state) + 1)}

    def new_states(self, state, action):
        return {state - action, state + action}

    def probability(self, state, action, new_state):
        return self.p if new_state > state else 1 - self.p

    def reward(self, state, action, new_state):
        return 1 if new_state == self.limit else 0

    def value_action(self, state, action):
        return sum(self.probability(state, action, new_state) *
                   (self.reward(state, action, new_state)
                    + self.gamma * self.values[new_state])
                   for new_state in self.new_states(state, action))

    def value_iteration(self, delta0):
        delta = 2 * delta0
        while delta0 < delta:
            delta = 0
            for state in self.states:
                value = self.values[state]
                self.values[state] = max(self.value_action(state, action) for action in self.actions(state))
                delta = max(delta, abs(value - self.values[state]))

    def update_policy(self):
        for state in self.states:
            max_action = None
            max_value = None
            for action in self.actions(state):
                if max_action is None:
                    max_action = action
                    max_value = self.value_action(state, action)
                else:
                    if self.value_action(state, action) > max_value:
                        max_action = action
                        max_value = self.value_action(state, action)
            self.policy[state] = max_action


if __name__ == "__main__":
    limit = 100
    accuracy = 0.00000001
    for p in [0.4]:
        gambler = Gambler(limit, p)

        gambler.value_iteration(accuracy)
        gambler.update_policy()

        x = list(range(1, limit))
        y = list(range(1, limit))
        for state, action in gambler.policy.items():
            y[state-1] = action

        plt.plot(x, y, label=f"p: {p}\nlim: {limit}\nacc: {accuracy}")

    plt.xlabel("purse")
    plt.ylabel("policy")
    plt.legend()
    plt.show()
