import pylab
import numpy

from MonteCarloMethods.Blackjack.Blackjack import Blackjack
from MonteCarloMethods.Blackjack.Dealer import Dealer
from MonteCarloMethods.Blackjack.Gambler import Gambler
from MonteCarloMethods.Blackjack.Policy import Policy
from MonteCarloMethods.Blackjack.State import State


class Game(object):
    def __init__(self, policy):
        self._policy = policy
        self.blackjack = Blackjack()
        self.gambler = Gambler(self.blackjack, policy)
        self.dealer = Dealer(self.blackjack)

    def play(self, mode):
        self.blackjack.hand()
        if mode == "comp":
            last_action = "stick"
            while self.gambler.move() == "hit":
                self.blackjack.hit(Gambler.__name__)
                if Blackjack.limit < self.blackjack.score(Gambler.__name__):
                    last_action = "hit"
                    break
                else:
                    self._policy.update(self.gambler.state(-1), "hit", 0)
        # elif mode == "player":
        #     self.gambler.player_move()
        else:
            raise AssertionError("Wrong mode")
        self.dealer.move()
        if mode == "comp":
            if last_action == "stick":
                self._policy.update(self.gambler.state(), "stick", self.blackjack.result())
            else:
                self._policy.update(self.gambler.state(-1), "hit", self.blackjack.result())
        return self.blackjack.result()

    def __str__(self):
        return str(self.blackjack)


if __name__ == "__main__":
    eps = 0.1
    count = 1000000
    limit = count // 2
    gambler_wins = 0
    dealer_wins = 0

    policy = Policy(eps)
    for i in range(count):
        game = Game(policy)
        res = game.play("comp")
        if i == limit:
            policy.eps = 0.
        if i > limit:
            if res == Gambler.__name__:
                gambler_wins += 1
            elif res == Dealer.__name__:
                dealer_wins += 1
        else:
            policy.eps = eps * (limit - i) / limit
        if i != limit and count >= 100 and i % (count // 100) == 0:
            print(f"complete: {100 * i // count}%")
            if i > limit:
                print(f"dealer wins: {100 * dealer_wins / (i - limit)}%")
                print(f"gambler wins: {100 * gambler_wins / (i - limit)}%")
    print("Total:")
    print(f"dealer wins: {100 * dealer_wins / (count - limit)}%")
    print(f"gambler wins: {100 * gambler_wins / (count - limit)}%")

    x = range(12, 22, 1)
    y = range(2, 12, 1)
    xgrid, ygrid = numpy.meshgrid(x, y)
    zgrid_usable = numpy.array([[policy._quatilies[(State(score, enemy_card, True))]["stick"]
                                     - policy._quatilies[(State(score, enemy_card, True))]["hit"]
                                     for score in x] for enemy_card in y])
    zgrid_non_usable = numpy.array([[policy._quatilies[(State(score, enemy_card, False))]["stick"]
                                         - policy._quatilies[(State(score, enemy_card, False))]["hit"]
                                         for score in x] for enemy_card in y])

    fig = pylab.figure()

    plt1 = fig.add_subplot(211, projection="3d", xlabel="score", ylabel="card value", title="usable ace, stick - hit")
    plt3 = fig.add_subplot(212, projection="3d", xlabel="score", ylabel="card value", title="no usable ace, stick - hit")

    plt1.plot_surface(xgrid, ygrid, zgrid_usable, cmap=pylab.cm.coolwarm)
    plt3.plot_surface(xgrid, ygrid, zgrid_non_usable, cmap=pylab.cm.coolwarm)
    pylab.show()

    print(policy)