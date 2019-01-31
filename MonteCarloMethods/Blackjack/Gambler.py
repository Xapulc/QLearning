from Player import Player


class Gambler(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self._value_limit = 20

    def move(self):
        while self._game.points(str(Gambler)) < self._value_limit:
            self._game.hit(str(Gambler))
