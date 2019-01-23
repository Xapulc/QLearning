import numpy as np
from math import sqrt


def create_data(n, count, expectations, variance):
    res = np.array([np.random.normal(expectations[i], sqrt(variance), count) for i in range(n)])
    return res.T
