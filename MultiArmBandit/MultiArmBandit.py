import matplotlib.pyplot as plt
import numpy as np
from math import e
from data_creater import create_data


class Bandit:
    def __init__(self, n):
        self.Q = np.zeros(n)
        self.Q_changes = np.zeros(n)
        self.n = n
        self.reference = 0
        self.p = np.empty(self.n)
        self.pi = np.empty(self.n)

    def optimistic(self):
        self.Q.fill(5)

    def change_Q(self, index, res):
        self.Q_changes[index] += 1
        self.Q[index] += (res - self.Q[index]) / (1 + self.Q_changes[index])

    def change_p(self, index, res, beta):
        self.p[index] += beta * (res-self.reference)

    def change_pi(self, index, beta):
        for i, pi in enumerate(self.pi):
            self.pi[i] += beta * ((1 if i == index else 0) - pi)

    def change_reference(self, res, alpha):
        self.reference += alpha * (res - self.reference)

    def soft_max(self, arr, t):
        gibbs_distrib = [e ** (arr[i] / t) for i in range(n)]
        elem = np.random.choice(arr, p=[gibbs_distrib[i] / sum(gibbs_distrib) for i in range(n)])
        return np.where(arr == elem)[0][0]

    def epsilon_greedy(self, epsilon):
        def helper(data):
            a = np.random.random()
            index = np.random.choice(range(self.n)) if a <= epsilon else self.Q.argmax()
            res = data[index]
            self.change_Q(index, res)
            return index

        return helper

    def soft_max_method(self, t):
        def helper(data):
            index = self.soft_max(self.Q, t)
            res = data[index]
            self.change_Q(index, res)
            return index

        return helper

    def comp_with_reinforcement(self, alpha, beta):
        def helper(data):
            index = self.soft_max(self.p, 1)
            res = data[index]
            self.change_p(index, res, beta)
            self.change_reference(res, alpha)
            return index

        return helper

    def pursuit(self, beta):
        def helper(data):
            index = self.pi.argmax()
            res = data[index]
            self.change_Q(index, res)
            ind_greedy = self.Q.argmax()
            self.change_pi(ind_greedy, beta)
            return index

        return helper

    def learn(self, **kwargs):
        def calc_accuracy(data, res):
            if data.min() == data.max():
                return 1
            else:
                return (res - data.min())/(data.max()-data.min())

        if kwargs["method"] == "epsilon_greedy":
            move = self.epsilon_greedy(kwargs["epsilon"])
        elif kwargs["method"] == "soft_max_method":
            move = self.soft_max_method(kwargs["t"])
        elif kwargs["method"] == "comp_with_reinforcement":
            self.p.fill(1/self.n)
            move = self.comp_with_reinforcement(kwargs["alpha"], kwargs["beta"])
        elif kwargs["method"] == "pursuit":
            self.pi.fill(1/self.n)
            move = self.pursuit(kwargs["beta"])
        else:
            raise TypeError

        if "optimistic" in kwargs.keys() and kwargs["optimistic"]:
            self.optimistic()

        data = kwargs["data"]
        accuracy = np.zeros(len(data) + 1)

        for k in range(len(data)):
            index = move(data[k])
            res = data[k][index]

            new_accuracy = (accuracy[k]*k + calc_accuracy(data[k], res)) / (k + 1)
            accuracy[k+1] = new_accuracy
        return accuracy

    def test(self, data):
        res = []
        for k in range(len(data[0])):
            index = self.Q.argmax()
            game_res = data[k][index]
            res.append(game_res)

        return res


if __name__ == "__main__":
    n = 10000
    count_learn = 100
    variance = 10

    expectations = np.random.normal(0, 1, n)
    data = create_data(n, count_learn, expectations, variance)

    bandits_eps = Bandit(n)
    bandits_soft = Bandit(n)

    for eps in [0.01]:
        plt.plot(range(count_learn), Bandit(n).learn(method="epsilon_greedy", data=data,
                                                     epsilon=eps, optimistic=True)[1:],
                 label=f'Opt eps={eps}')
    for t in [0.1]:
        plt.plot(range(count_learn), Bandit(n).learn(method="soft_max_method", data=data,
                                                     t=t, optimistic=True)[1:],
                 label=f'Opt t={t}')
    for alpha in [0.1]:
        for beta in [1]:
            plt.plot(range(count_learn), Bandit(n).learn(method="comp_with_reinforcement", data=data,
                                                         alpha=alpha, beta=beta)[1:],
                     label=f'Alpha={alpha}, beta={beta}')
    for beta in [0.01]:
        plt.plot(range(count_learn), Bandit(n).learn(method="pursuit", data=data,
                                                     beta=beta)[1:],
                 label=f'Beta={beta}')

    plt.xlabel("game")
    plt.ylabel("accuracy")
    plt.legend()
    plt.show()
