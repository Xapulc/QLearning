class State(object):
    def __init__(self, score, enemy_card, is_usable_ace_exist):
        self.score = score
        if type(enemy_card).__name__ == "Card":
            self.enemy_card = enemy_card.value
        else:
            self.enemy_card = enemy_card
        self.is_usable_ace_exist = is_usable_ace_exist

    def __eq__(self, other):
        return self.score == other.score and self.enemy_card == other.enemy_card \
               and self.is_usable_ace_exist == other.is_usable_ace_exist

    def __hash__(self):
        # print(type(self.score), type(hash(self.enemy_card)), type(hash(self.is_usable_ace_exist)))
        # print((self.score - 12) + 10 * self.enemy_card + 100 * hash(self.is_usable_ace_exist))
        return (self.score - 2) + 21 * (hash(self.enemy_card) - 2) + 21 * 11 * hash(self.is_usable_ace_exist)

    def __str__(self):
        res = ""
        res += f"Score: {self.score}, enemy card: {str(self.enemy_card)}, "
        res += "usable ace " + ("" if self.is_usable_ace_exist else "does not ") + "exist"
        return res