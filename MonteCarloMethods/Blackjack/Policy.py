from random import choice, random, randint

from MonteCarloMethods.Blackjack.Card import Card
from MonteCarloMethods.Blackjack.Blackjack import Blackjack
from MonteCarloMethods.Blackjack.State import State

from MonteCarloMethods.Blackjack.Gambler import Gambler


class Policy(object):
    def __init__(self, eps=0):
        self.eps = eps
        self._states = set()
        for score in range(2, Blackjack.limit + 1):
            for enemy_card in Card.get_possible_choice():
                for is_usable_ace_exist in (False, True):
                    self._states.add(State(score, enemy_card, is_usable_ace_exist))

        self._actions = {state: {"hit", "stick"} for state in self._states}

        self._values = {state: 0 for state in self._states}
        self._quatilies = {state: {action: 0 for action in self._actions[state]} for state in self._states}
        self._policy = {state: choice(list(self._actions[state])) if state.score >= 12 else "hit" for state in
                        self._states}
        self._results = {state: {action: [] for action in self._actions[state]} for state in self._states}

    def move(self, state):
        return self._policy[state]

    def argmax_qualities(self, state):
        max_quality = None
        max_action = None

        for action in self._actions[state]:
            if max_quality is None:
                max_action = action
                max_quality = self._quatilies[state][action]
            else:
                if max_quality < self._quatilies[state][action]:
                    max_action = action
                    max_quality = self._quatilies[state][action]
        return max_action

    def update(self, state, action, result):
        if type(result).__name__ == "int":
            res = result
        elif result == Gambler.__name__:
            res = 1
        elif result == "push":
            res = 0
        else:
            res = -1

        self._results[state][action].append(res)
        self._quatilies[state][action] = sum(self._results[state][action]) / len(self._results[state][action])

        rnd = random()
        self._policy[state] = self.argmax_qualities(state) if rnd > self.eps else choice(list(self._actions[state]))

    def __str__(self):
        res_unable = [[self._policy[State(score, card_value, True)][0] for card_value in range(2, 11)]
                      for score in range(2, Blackjack.limit + 1)]
        res_non_unable = [[self._policy[State(score, card_value, False)][0] for card_value in range(2, 11)]
                          for score in range(2, Blackjack.limit + 1)]
        return "unable\n" + "\n".join(" ".join(res_unable[k]) for k in range(19)) + "\nnon enable\n" + "\n".join(
            " ".join(res_non_unable[k]) for k in range(19))
