from Player import Player


class Gambler(Player):
    def __init__(self, game):
        Player.__init__(self, game)
        self._value_limit = 20

    def comp_move(self):
        while self._game.points(str(Gambler)) < self._value_limit:
            self._game.hit(str(Gambler))

    def player_move(self):
        print(self._game.get_game(str(Gambler)))
        while True:
            step = input("Choose hit or stick")
            if step == "hit":
                self._game.hit(str(Gambler))
                print(self._game.get_game(str(Gambler)))
                if self._game.points(str(Gambler)) >= 21:
                    break
            elif step == "stick":
                break
            else:
                print("Wrong enter")
