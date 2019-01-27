from math import e


def fact(n):
    return n*fact(n-1) if n > 0 else 1


def puasson(n, E):
    return (E ** n) * (e ** (-E)) / (fact(n))
