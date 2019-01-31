from Player import Player


class Dealer(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self._value_limit = 17

    def move(self):
        while self._game.points(str(Dealer)) < self._value_limit:
            self._game.hit(str(Dealer))
