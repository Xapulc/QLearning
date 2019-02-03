from MonteCarloMethods.Blackjack.Player import Player


class Gambler(Player):
    def __init__(self, game, policy=None):
        Player.__init__(self, game)
        self._policy = policy

    def move(self):
        return self._policy.move(self.state())

    def state(self, num=None):
        return self._game.get_state(Gambler.__name__, num)

    def player_move(self):
        print(self._game.get_game(Gambler.__name__))
        while True:
            step = input("Choose hit or stick")
            if step in {"hit", "stick"}:
                return step
            else:
                print("Wrong enter")
            if step == "hit":
                self._game.hit(Gambler.__name__)
                print(self._game.get_game(Gambler.__name__))
                if self._game.score(Gambler.__name__) >= 21:
                    break
            elif step == "stick":
                break
