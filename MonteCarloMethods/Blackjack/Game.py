from Blackjack import Blackjack
from Dealer import Dealer
from Gambler import Gambler


class Game(object):
    def __init__(self):
        self.blackjack = Blackjack()
        self.gambler = Gambler(self.blackjack)
        self.dealer = Dealer(self.blackjack)

    def play(self, mode):
        self.blackjack.hand()
        if mode == "comp":
            self.gambler.comp_move()
        elif mode == "player":
            self.gambler.player_move()
        else:
            raise AssertionError("Wrong mode")
        self.dealer.move()
        return self.blackjack.result()

    def __str__(self):
        return str(self.blackjack)


if __name__ == "__main__":
    game = Game()
    res = game.play("player")
    print(game)
    print(f"Res: {res}")