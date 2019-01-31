import abc

class Player(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, game):
        self._game = game

    def __str__(cls):
        return cls.__name__()

    @abc.abstractmethod
    def move(self):
        pass
