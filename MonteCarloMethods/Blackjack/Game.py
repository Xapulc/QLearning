import pylab
from mpl_toolkits.mplot3d import Axes3D
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
            while self.gambler.move() == "hit":
                if Blackjack.limit >= self.blackjack.score(Gambler.__name__):
                    self._policy.update(self.gambler.state(-1), "hit", 0)
                else:
                    last_action = "hit"
                    break
            else:
                last_action = "stick"
        elif mode == "player":
            self.gambler.player_move()
        else:
            raise AssertionError("Wrong mode")
        self.dealer.move()
        if mode == "comp":
            self._policy.update(self.gambler.state(-1), last_action, self.blackjack.result())
        return self.blackjack.result()

    def __str__(self):
        return str(self.blackjack)


if __name__ == "__main__":
    policy = Policy()
    for _ in range(50000):
        game = Game(policy)
        res = game.play("comp")

    x = range(12, 22, 1)
    y = range(2, 12, 1)
    xgrid, ygrid = numpy.meshgrid(x, y)
    zgrid_usable = numpy.array([[1 if policy.move(State(score, enemy_card, True)) == "hit" else 0
                                 for score in x] for enemy_card in y])
    zgrid_non_usable = numpy.array([[1 if policy.move(State(score, enemy_card, False)) == "hit" else 0
                                     for score in x] for enemy_card in y])

    fig = pylab.figure()

    plt1 = fig.add_subplot(211, projection="3d", xlabel="score", ylabel="card value", title="usable ace")
    plt2 = fig.add_subplot(212, projection="3d", xlabel="score", ylabel="card value", title="no usable ace")

    plt1.plot_surface(xgrid, ygrid, zgrid_usable, cmap=pylab.cm.Spectral)
    plt2.plot_surface(xgrid, ygrid, zgrid_non_usable, cmap=pylab.cm.Spectral)
    pylab.show()
