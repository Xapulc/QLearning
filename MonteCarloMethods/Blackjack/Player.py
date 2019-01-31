import abc


class Player(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game):
        self._game = game
        self._enemy_card = None
        self._cards = []

    @abc.abstractmethod
    def move(self):
        pass
