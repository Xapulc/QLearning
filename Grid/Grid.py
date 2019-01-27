import numpy as np
from time import time
from I2Point import I2Point


class Grid(object):
    def __init__(self, size=4, gamma=1.):
        self.Splus = np.zeros((size, size))
        self.strategies = [[None for _ in range(size)] for _ in range(size)]
        self.size = size
        self.gamma = gamma
        self.terminal = (I2Point(0, 0), I2Point(self.size - 1, self.size - 1))

    def set_strategies(self):
        for i in range(self.size):
            for j in range(self.size):
                value = max([self.Splus[pt.x, pt.y] for pt in self.get_transitions(I2Point(i, j))])
                self.strategies[i][j] = np.array([pt for pt in self.get_transitions(I2Point(i, j))
                                                  if value == self.Splus[pt.x, pt.y]])

    def prob_strategies(self, cur, next):
        if next in self.strategies[cur.x][cur.y]:
            return 1 / len(self.strategies[cur.x][cur.y])
        else:
            return 0

    def IES(self, delta0):
        """
        Iteration Estimate Strategies
        :return:
        """
        delta = 2 * delta0

        while delta0 < delta:
            delta = 0
            for i in range(self.size):
                for j in range(self.size):
                    if I2Point(i, j) not in self.terminal:
                        v = self.Splus[i, j].copy()
                        sm = 0
                        for pt in self.get_transitions(I2Point(i, j)):
                            sm += self.prob_strategies(I2Point(i, j), pt) * (-1 + self.gamma * self.Splus[pt.x, pt.y])
                        self.Splus[i, j] = sm
                        delta = max(delta, abs(v - self.Splus[i, j]))

    def get_transitions(self, pt):
        dx = I2Point(1, 0)
        dy = I2Point(0, 1)
        if pt.x != 0:
            yield pt - dx
        if pt.x != self.size - 1:
            yield pt + dx
        if pt.y != 0:
            yield pt - dy
        if pt.y != self.size - 1:
            yield pt + dy

    def __str__(self):
        strings = ["" for _ in range(self.size*4 + 1)]
        for i in range(self.size + 1):
            strings[4*i] += "".join(["-" for _ in range(self.size*4 + 1)])
        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    for k in range(1, 4):
                        strings[4*i+k] += "|"
                if i != 0 and I2Point(i - 1, j) in self.strategies[i][j]:
                    strings[4*i+1] += " ^ "
                else:
                    strings[4*i+1] += "   "

                if j != 0 and I2Point(i, j - 1) in self.strategies[i][j]:
                    strings[4*i+2] += "< "
                else:
                    strings[4*i+2] += "  "

                if j != self.size-1 and I2Point(i, j + 1) in self.strategies[i][j]:
                    strings[4*i+2] += ">"
                else:
                    strings[4*i+2] += " "

                if i != self.size-1 and I2Point(i + 1, j) in self.strategies[i][j]:
                    strings[4*i+3] += " v "
                else:
                    strings[4*i+3] += "   "

                for k in range(1, 4):
                    strings[4*i+k] += "|"

        return "\n".join(strings)


if __name__ == "__main__":
    grid = Grid(1000)
    start = time()
    grid.set_strategies()
    grid.IES(0.002)
    grid.set_strategies()
    end = time()
    print(end - start)
    # print(grid)
