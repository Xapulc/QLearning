class Card(object):
    _possible_choice = {str(val) for val in range(2, 11)}.union({"J", "Q", "K", "A"})

    def __init__(self, name):
        assert name in Card._possible_choice, "Wrong name"
        self._name = name

    @classmethod
    def get_possible_choice(cls):
        return {Card(name) for name in cls._possible_choice}

    def __hash__(self):
        return hash(self._name)

    def name(self):
        return self._name

    def __str__(self):
        return f"{self._name}"
