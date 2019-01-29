class I2Point(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __copy__(self):
        return I2Point(self.x, self.y)

    def __add__(self, other):
        return I2Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return I2Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"