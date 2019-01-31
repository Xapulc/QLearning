from Player import Player


class Gambler(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self._value_limit = 20

    def comp_move(self):
        while self._game.points(Gambler.__name__) < self._value_limit:
            self._game.hit(Gambler.__name__)

    def player_move(self):
        print(self._game.get_game(Gambler.__name__))
        while True:
            step = input("Choose hit or stick")
            if step == "hit":
                self._game.hit(Gambler.__name__)
                print(self._game.get_game(Gambler.__name__))
                if self._game.points(Gambler.__name__) >= 21:
                    break
            elif step == "stick":
                break
            else:
                print("Wrong enter")
