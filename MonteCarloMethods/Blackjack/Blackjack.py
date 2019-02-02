from random import choice

from MonteCarloMethods.Blackjack.State import State
from MonteCarloMethods.Blackjack.Card import Card
from MonteCarloMethods.Blackjack.Dealer import Dealer
from MonteCarloMethods.Blackjack.Gambler import Gambler


class Blackjack(object):
    limit = 21

    def __init__(self):
        self._cards = Card.get_possible_choice()
        self._dealer = Dealer.__name__
        self._gambler = Gambler.__name__
        self._gambler_cards = []
        self._dealer_cards = []

    def get_enemy_card(self, turn):
        if turn == self._gambler:
            return self._dealer_cards[0]
        elif turn == self._dealer:
            return self._gambler_cards[0]
        else:
            raise AssertionError("Wrong player's name")

    def get_cards(self, turn):
        if turn == self._gambler:
            return self._gambler_cards
        elif turn == self._dealer:
            return self._dealer_cards
        else:
            raise AssertionError("Wrong player's name")

    def get_game(self, turn):
        return self.__str__(turn)

    def get_state(self, turn, num=None):
        if num is not None:
            if turn == self._gambler:
                buf = self._gambler_cards.copy()
                self._gambler_cards = self._gambler_cards[:num]
            elif turn == self._dealer:
                buf = self._dealer_cards.copy()
                self._dealer_cards = self._dealer_cards[:num]
            else:
                AssertionError("Wrong player's name")
        state = State(self.score(turn), self.get_enemy_card(turn), self.is_usable_ace_exist(turn))
        if num is not None:
            if turn == self._gambler:
                self._gambler_cards = buf
            else:
                self._dealer_cards = buf

        return state

    def _helper_for_score(self, cards):
        sm = 0
        ace_count = 0
        for card in cards:
            if card.name() in {str(val): val for val in range(2, 11)}:
                sm += int(card.name())
            elif card.name() in {"J", "Q", "K"}:
                sm += 10
            elif card.name() == "A":
                ace_count += 1

        usable_ace_count = max(min(ace_count, (Blackjack.limit - sm - ace_count) // 10), 0)
        return sm, ace_count, usable_ace_count

    def score(self, turn):
        """
        I find score of cards as sum of card values
        If card name in {"2", .. , "10"}, then value equals card name
        If card name in {"J", "Q", "K"}, then value equals 10
        If card name is A, then value equals 1 or 11, which depends from sum of other cards
        So as to find usable ace count (which values equals 11), we find max value k, which satisfy next equations
        sum + ace_count - k + 11 * k < self.limit
        0 <= k <= ace_count
        :param turn: who will comp_move
        :return: score of cards
        """
        cards = self.get_cards(turn)
        sm, ace_count, usable_ace_count = self._helper_for_score(cards)
        return sm + (ace_count - usable_ace_count) + (11 * usable_ace_count)

    def is_usable_ace_exist(self, turn):
        cards = self.get_cards(turn)
        sm, ace_count, usable_ace_count = self._helper_for_score(cards)
        return usable_ace_count > 0

    def hit(self, turn):
        cards = self.get_cards(turn)
        assert self.score(turn) <= Blackjack.limit, "So many cards"
        rnd_card = choice(list(self._cards))
        cards.append(rnd_card)
        return rnd_card

    def hand(self):
        self.hit(self._gambler)
        self.hit(self._dealer)
        self.hit(self._gambler)
        self.hit(self._dealer)

    def result(self):
        if self.score(self._gambler) > Blackjack.limit:
            return self._dealer
        elif self.score(self._dealer) > Blackjack.limit:
            return self._gambler
        elif self.score(self._gambler) > self.score(self._dealer):
            return self._gambler
        elif self.score(self._gambler) < self.score(self._dealer):
            return self._dealer
        else:
            return "push"

    def __str__(self, turn=None):
        res = "-------\n"
        for player, cards in [(self._gambler, self._gambler_cards), (self._dealer, self._dealer_cards)]:
            res += f"{player}:\n"
            res += f"Vis: {cards[0]}\n"
            if not turn or turn == player:
                res += f"Inv: {', '.join(str(card) for card in cards[1:])}\n"
                res += f"Sc: {self.score(player)}\n"
                res += "-------\n"
        return res
