from MonteCarloMethods.Blackjack.Card import Card
from MonteCarloMethods.Blackjack.Blackjack import Blackjack
from MonteCarloMethods.Blackjack.State import State

from MonteCarloMethods.Blackjack.Gambler import Gambler


class Policy(object):
    def __init__(self):
        self._states = set()
        for score in range(2, Blackjack.limit + 1):
            for enemy_card in Card.get_possible_choice():
                for is_usable_ace_exist in (False, True):
                    self._states.add(State(score, enemy_card, is_usable_ace_exist))

        self._values = {state: 0 for state in self._states}
        self._count_games = {state: 0 for state in self._states}

    def move(self, state):
        if state.score < 20:
            return "hit"
        else:
            return "stick"

    def update_values(self, state, result):
        if result == Gambler.__name__:
            res = 1
        elif result == "push":
            res = 0
        else:
            res = -1

        self._count_games[state] += 1
        self._values[state] = ((self._count_games[state]-1) * self._values[state] + res) \
                              / self._count_games[state]
