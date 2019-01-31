import abc


class Player(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game):
        self._game = game
        self._enemy_card = None
        self._cards = []

    def __str__(cls):
        return cls.__name__()

    @abc.abstractmethod
    def move(self):
        pass
